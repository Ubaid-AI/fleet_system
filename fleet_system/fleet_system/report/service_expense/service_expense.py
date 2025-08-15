# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns()
	data = get_vehicle_log_data(filters)
	# chart = get_chart_data(data, filters)

	return columns, data, None
	# , chart

def get_columns():
	return [
		{
			'fieldname': 'license_plate',
			'fieldtype': 'Link',
			'label': _('Vehicle'),
			'options': 'Vehicle',
			'width': 150
		},
		
		{
			'fieldname': 'make',
			'fieldtype': 'Data',
			'label': _('Make'),
			'width': 80
		},
		{
			'fieldname': 'model',
			'fieldtype': 'Data',
			'label': _('Model'),
			'width': 100
		},
		{
			'fieldname':'date',
			'fieldtype':'date',
			'label':'Date',
			'width':50
		},
		{
			'fieldname': 'supplier',
			'fieldtype': 'Data',
			'label': _('Supplier'),
			'width': 100
		},
		{
			'fieldname': 'type',
			'fieldtype': 'Data',
			'label': _('Type'),
			'width': 80
		},
		{
			'fieldname': 'service_item',
			'fieldtype': 'Data',
			'label': _('Service Item'),
			'width': 100
		},
		{
			'fieldname': 'expense_amount',
			'fieldtype': 'Currency',
			'label': _('Expense Amount'),
			'width': 150
		}
	]


def get_vehicle_log_data(filters):
	start_date, end_date = get_period_dates(filters)
	conditions, values = get_conditions(filters)

	data = frappe.db.sql("""
		# SELECT
		# 	vhcl.license_plate as vehicle, vhcl.make, vhcl.model,
		# 	vhcl.location, log.name as log_name, log.odometer,
		# 	log.date, log.employee, log.fuel_qty,
		# 	log.price as fuel_price,
		# 	log.fuel_qty * log.price as fuel_expense
		# FROM
		# 	`tabVehicle` vhcl,`tabVehicle Log` log
		# WHERE
		# 	vhcl.license_plate = log.license_plate
		# 	and log.docstatus = 1



		SELECT  
			log.license_plate,
			log.make,
			log.model,
			log.date,
			vs.supplier,
			vs.service_item,
			vs.type,
			vs.expense_amount
			from
			`tabVehicle Service` vs, `tabVehicle Log` log
			where
			log.name = vs.parent
			and log.date between %(start_date)s and %(end_date)s
			{0}
		ORDER BY log.date""".format(conditions), values, as_dict=1)

	# for row in data:
	# 	# row['service_expense'] = get_service_expense(row.log_name)

	return data


def get_conditions(filters):
	conditions = ''

	start_date, end_date = get_period_dates(filters)
	values = {
		'start_date': start_date,
		'end_date': end_date
	}

	if filters.license_plate:
		conditions += ' and log.license_plate = %(license_plate)s'
		values['license_plate'] = filters.license_plate

	return conditions, values


def get_period_dates(filters):
	if filters.filter_based_on == 'Fiscal Year' and filters.fiscal_year:
		fy = frappe.db.get_value('Fiscal Year', filters.fiscal_year,
			['year_start_date', 'year_end_date'], as_dict=True)
		return fy.year_start_date, fy.year_end_date
	else:
		return filters.from_date, filters.to_date