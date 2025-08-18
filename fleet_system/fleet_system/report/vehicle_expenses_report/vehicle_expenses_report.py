# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe

# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt

from erpnext.accounts.report.financial_statements import get_period_list


def execute(filters=None):
	filters = frappe._dict(filters or {})

	columns = get_columns()
	data = get_vehicle_log_data(filters)
	chart = get_chart_data(data, filters)

	return columns, data, None, chart

def get_columns():
	return [
		{
			'fieldname': 'employee',
			'fieldtype': 'Link',
			'label': _('Employee'),
			'options': 'Employee',
			'width': 225
		},
		{
			'fieldname': 'vehicle',
			'fieldtype': 'Link',
			'label': _('Vehicle'),
			'options': 'Vehicle',
			'width': 90
		},
		{
			'fieldname': 'make',
			'fieldtype': 'Data',
			'label': _('Make'),
			'width': 70
		},
		{
			'fieldname': 'model',
			'fieldtype': 'Data',
			'label': _('Model'),
			'width': 80
		},
		{
			'fieldname': 'log_name',
			'fieldtype': 'Link',
			'label': _('Vehicle Log'),
			'options': 'Vehicle Log',
			'width': 100
		},
		{
			'fieldname': 'odometer',
			'fieldtype': 'Int',
			'label': _('Odometer Value'),
			'width': 80
		},
		{
			'fieldname': 'date',
			'fieldtype': 'Date',
			'label': _('Date'),
			'width': 100
		},
		{
			'fieldname': 'fuel_qty',
			'fieldtype': 'Float',
			'label': _('Fuel Qty'),
			'width': 80
		},
		{
			'fieldname': 'fuel_price',
			'fieldtype': 'Float',
			'label': _('Fuel Price/Ltr'),
			'width': 100
		},
		{
			'fieldname': 'fuel_expense',
			'fieldtype': 'Currency',
			'label': _('Fuel Expense'),
			'width': 110
		},
		{
			'fieldname': 'service_expense',
			'fieldtype': 'Link',
			'options': 'Vehicle Service',			
			'label': _('Service Expense'),
			'width': 110
		}

		# ,
		# {
		# 	'fieldname': 'employee_name',
		# 	'fieldtype': 'Data',
		# 	'label': _('Employee Name'),
		# 	'width': 100
		# }
	]


def get_vehicle_log_data(filters):
	start_date, end_date = get_period_dates(filters)
	conditions, values = get_conditions(filters)

	data = frappe.db.sql("""
		SELECT
			vhcl.license_plate as vehicle, vhcl.make, vhcl.model,
			vhcl.location, log.name as log_name, log.odometer,
			log.date, log.employee, log.fuel_qty,
			log.price as fuel_price,
			log.fuel_qty * log.price as fuel_expense,
			emp.employee_name
		FROM
			`tabFleet Vehicle` vhcl,`tabVehicle Log` log , `tabEmployee` emp
		WHERE
			vhcl.license_plate = log.license_plate
			and log.employee = emp.employee_number
			and log.docstatus = 1
			and date between %(start_date)s and %(end_date)s
			{0}
		ORDER BY date""".format(conditions), values, as_dict=1)

	for row in data:
		row['service_expense'] = get_service_expense(row.log_name)
		row['indent'] = 0

	return data


def get_conditions(filters):
	conditions = ''

	start_date, end_date = get_period_dates(filters)
	values = {
		'start_date': start_date,
		'end_date': end_date
	}

	if filters.employee:
		conditions += ' and log.employee = %(employee)s'
		values['employee'] = filters.employee

	if filters.vehicle:
		conditions += ' and vhcl.license_plate = %(vehicle)s'
		values['vehicle'] = filters.vehicle

	return conditions, values


# apps/fleet_system/.../vehicle_expenses.py

from frappe.utils import getdate, nowdate
import frappe

def get_period_dates(filters):
    # 1) Date Range explicitly selected
    if filters.get("filter_based_on") == "Date Range":
        if not (filters.get("from_date") and filters.get("to_date")):
            frappe.throw("Please set both From Date and To Date.")
        return getdate(filters.from_date), getdate(filters.to_date)

    # 2) Fiscal Year selected -> try to load it
    fy_name = (filters.get("fiscal_year") or "").strip()
    if fy_name:
        fy = frappe.db.get_value(
            "Fiscal Year",
            {"name": fy_name},
            ["year_start_date", "year_end_date"],
            as_dict=True,
        )
        if fy:
            return fy["year_start_date"], fy["year_end_date"]

        # Either be strict...
        # frappe.throw(f"Fiscal Year '{fy_name}' not found.")
        # ...or be forgiving and infer from dates/today. Pick one. Below is the forgiving path:

    # 3) Fallback: infer a fiscal year from a provided date or today
    try:
        from erpnext.accounts.utils import get_fiscal_year
        base_date = filters.get("from_date") or filters.get("to_date") or nowdate()
        _, year_start, year_end = get_fiscal_year(base_date)
        return year_start, year_end
    except Exception:
        # Last resort: if we can't infer, require date range
        frappe.throw("Select a valid Fiscal Year or switch filter to Date Range with From/To dates.")



def get_service_expense(logname):
	expense_amount = frappe.db.sql("""
		SELECT sum(expense_amount)
		FROM
			`tabVehicle Log` log, `tabVehicle Service` service
		WHERE
			service.parent=log.name and log.name=%s
	""", logname)

	return expense_amount[0][0] if expense_amount else 0.0


def get_chart_data(data, filters):
	period_list = get_period_list(filters.fiscal_year, filters.fiscal_year,
		filters.from_date, filters.to_date, filters.filter_based_on, 'Monthly')

	fuel_data, service_data = [], []

	for period in period_list:
		total_fuel_exp = 0
		total_service_exp = 0

		for row in data:
			if row.date <= period.to_date and row.date >= period.from_date:
				total_fuel_exp += flt(row.fuel_expense)
				total_service_exp += flt(row.service_expense)

		fuel_data.append([period.key, total_fuel_exp])
		service_data.append([period.key, total_service_exp])

	labels = [period.label for period in period_list]
	fuel_exp_data= [row[1] for row in fuel_data]
	service_exp_data= [row[1] for row in service_data]

	datasets = []
	if fuel_exp_data:
		datasets.append({
			'name': _('Fuel Expenses'),
			'values': fuel_exp_data
		})

	if service_exp_data:
		datasets.append({
			'name': _('Service Expenses'),
			'values': service_exp_data
		})

	chart = {
		'data': {
			'labels': labels,
			'datasets': datasets
		},
		'type': 'line',
		'fieldtype': 'Currency'
	}

	return chart
