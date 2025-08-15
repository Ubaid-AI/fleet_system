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
	# chart = get_chart_data(data, filters)
	# report_summary = get_summary_report(data,filters)

	return columns, data, None , None
	# , report_summary
	# , chart

def get_columns():
	return [
		{
			'fieldname': 'license_plate',
			'fieldtype': 'Link',
			'label': _('Reg: No'),
			'options': 'Vehicle',
			'width': 100
		},
		{
			'fieldname': 'ownership',
			'fieldtype': 'Data',
			'label': _('Ownership'),
			'width': 70
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
			'fieldname': 'make_date',
			'fieldtype': 'Data',
			'label': _('Year'),
			'width': 55
		},
		{
			'fieldname': 'possession',
			'fieldtype': 'Data',
			'label': _('Possession'),
			'width': 120
		},
		# {
		# 	'fieldname': 'insurance_company',
		# 	'fieldtype': 'Data',
		# 	'label': _('Insurance Company'),
		# 	'width': 120
		# },
		{
			'fieldname': 'insurance_abr',
			'fieldtype': 'Data',
			'label': _('Insurance Company'),
			'width': 120
		},
		{
			'fieldname': 'vehicle_value',
			'fieldtype': 'Currency',
			'label': _('Purchase'),
			'width': 100
		},
		{
			'fieldname': 'tracker',
			'fieldtype': 'Data',
			'label': _('Tracker'),
			'width': 70
		},
		{
			'fieldname': 'sum_insured',
			'fieldtype': 'Currency',
			'label': _('Sum Insured'),
			'width': 100
		},
		{
			'fieldname': 'premium',
			'fieldtype': 'Currency',
			'label': _('Premium'),
			'width': 100
		},
		{
			'fieldname': 'rate',
			'fieldtype': 'Percent',
			'label': _('Rate'),
			'width': 100
		},
				{
			'fieldname': 'date',
			'fieldtype': 'Date',
			'label': _('Insurance Expiry'),
			'width': 120
		},
		{
			'fieldname': 'location',
			'fieldtype': 'Data',
			'label': _('Location'),
			'width': 70
		}
		
	]


def get_vehicle_log_data(filters):
	start_date, end_date = get_period_dates(filters)
	conditions, values = get_conditions(filters)

	# data = frappe.db.sql("""
	# SELECT v.employee, v.license_plate, v.make, v.model, v.make_date, v.employee_name, v.insurance_company, ic.short_title, v.vehicle_value, v.sum_insured, v.tracker, v.premium, v.rate, v.end_date as date,v.location,v.ownership
	# from `tabFleet Vehicle` v, `tabInsurance Company` ic 
	# WHERE
	# 	v.vehical_type = 'Car'
	# 	and v.end_date between %(start_date)s and %(end_date)s 
	# 	and v.insurance_company = ic.company_name
	# 	{0}
	# ORDER BY v.insurance_company, date""".format(conditions), values, as_dict=1)
	data = frappe.db.sql("""
		SELECT  ic.license_plate, ic.make, ic.model, v.make_date, ic.possession, ic.insurance_abr, v.vehicle_value,ic.insurance_company, ic.sum_insured, ic.tracker, ic.premium, ic.rate, ic.end_date as date, v.location, ic.ownership
		FROM `tabFleet Vehicle` v, `tabVehicle Insurance` ic 
		WHERE
			v.vehical_type = 'Car'
			and ic.end_date between SYSDATE() and %(end_date)s 
			and ic.license_plate = v.name
			{0}
		ORDER BY ic.insurance_company, date""".format(conditions), values, as_dict=1)
	not_in_insurance = frappe.db.sql(""" 
				SELECT v.license_plate, v.employee_name, v.ownership
			from `tabFleet Vehicle` v WHERE 		v.vehical_type = 'Car'
and  v.license_plate  Not in (SELECT license_plate from `tabVehicle Insurance`)""", as_dict=1)
	expired = frappe.db.sql(""" 
			SELECT DISTINCT ic.license_plate, ic.possession, ic.ownership, ic.end_date from  `tabVehicle Insurance` ic, `tabFleet Vehicle` v 
			WHERE v.vehical_type = 'Car' and ic.end_date < SYSDATE() and ic.license_plate not in 
			(SELECT license_plate from `tabVehicle Insurance` where end_date > SYSDATE())
			ORDER BY ic.end_date 
	""", as_dict=1)


	previous_insurance = '  '
	insurance_summary = []
	for row in data:
		row['make_date']= frappe.utils.formatdate(row['make_date'],"yyyy")
		current_insurance = row['insurance_company']
		if current_insurance == previous_insurance:
			insurance_summary[-1]['total'] += row['premium']
		else:
			insurance_summary.append({
				'name': current_insurance,
				'total': row['premium']				
			})
			previous_insurance = current_insurance
	if data:
		data[-1]['companies'] = insurance_summary
		data[-1]['expired'] = expired
		data[-1]['not_in'] = not_in_insurance
	del insurance_summary
	
	return data


def get_conditions(filters):
	conditions = ''

	# start_date, end_date = get_period_dates(filters)
	values = {
		'start_date': filters.start_date,
		'end_date': filters.to_date
	}

	if filters.employee:
		conditions += ' and ic.possession = %(possession)s'
		emp_name = frappe.db.sql(f"""SELECT e.employee_name from `tabEmployee` e WHERE e.employee={filters.employee}""")
		values['possession'] = emp_name[0][0]

	if filters.license_plate:
		conditions += ' and ic.license_plate = %(license_plate)s'
		values['license_plate'] = filters.license_plate
	
	if filters.insurance_company:
		conditions += ' and ic.insurance_abr = %(insurance_company)s'
		values['insurance_company'] = filters.insurance_company
	if filters.ownership:
		conditions += ' and ic.ownership = %(ownership)s'
		values['ownership'] = filters.ownership

	return conditions, values


def get_period_dates(filters):
	if filters.filter_based_on == 'Fiscal Year' and filters.fiscal_year:
		fy = frappe.db.get_value('Fiscal Year', filters.fiscal_year,
			['year_start_date', 'year_end_date'], as_dict=True)
		return fy.year_start_date, fy.year_end_date
	else:
		return filters.from_date, filters.to_date

# def get_summary_report(data,filters):
# 	report_summary = [
# 		{"label":"Insurance Company","value":data[-1].total,'indicator':'Red'},
# 		{"label":"dogs","value":3647,'indicator':'Blue'}
# 	]
# 	return report_summary
