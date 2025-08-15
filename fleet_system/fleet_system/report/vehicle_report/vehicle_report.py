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
			'fieldname': 'ownership',
			'fieldtype': 'Data',
			'label': _('Ownership'),
			'width': 70
		},
		{
			'fieldname': 'employee_name',
			'fieldtype': 'Data',
			'label': _('Possession'),
			'width': 120
		},
		{
			'fieldname': 'driver_name',
			'fieldtype': 'Data',
			'label': _('Driver'),
			'width': 120
		},
		{
			'fieldname': 'tracker',
			'fieldtype': 'Data',
			'label': _('Tracker'),
			'width': 120
		},
		{
			'fieldname': 'vehicle_value',
			'fieldtype': 'Currency',
			'label': _('Purchase'),
			'width': 100
		},
		{
			'fieldname': 'market_value',
			'fieldtype': 'Currency',
			'label': _('Market Value'),
			'width': 100
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

	data = frappe.db.sql("""
	SELECT DISTINCT v.employee, v.license_plate, v.make, v.model,v.make_date, v.employee_name,v.market_value, v.driver_name, v.vehicle_value, v.sum_insured, v.tracker, v.premium, v.rate,v.location,v.ownership
	from `tabFleet Vehicle` v, `tabInsurance Company` ic 
	WHERE
		v.vehical_type = 'Car'
		""".format(conditions), values, as_dict=1)
	previous_insurance = '  '
	insurance_summary = []
	for row in data:
		row['make_date']= frappe.utils.formatdate(row['make_date'],"yyyy")
	# 	current_insurance = row['insurance_company']
	# 	if current_insurance == previous_insurance:
	# 		insurance_summary[-1]['total'] += row['premium']
	# 	else:
	# 		insurance_summary.append({
	# 			'name': current_insurance,
	# 			'total': row['premium']				
	# 		})
	# 		previous_insurance = current_insurance
	# if data:
	# 	data[-1]['companies'] = insurance_summary
	# del insurance_summary
	
	return data


def get_conditions(filters):
	conditions = ''

	start_date, end_date = get_period_dates(filters)
	values = {
		'start_date': start_date,
		'end_date': end_date
	}

	if filters.employee:
		conditions += ' and v.employee = %(employee)s'
		values['employee'] = filters.employee

	if filters.license_plate:
		conditions += ' and v.license_plate = %(license_plate)s'
		values['license_plate'] = filters.license_plate
	
	# if filters.insurance_company:
	# 	conditions += ' and v.insurance_company = %(insurance_company)s'
	# 	values['insurance_company'] = filters.insurance_company
	if filters.ownership:
		conditions += ' and v.ownership = %(ownership)s'
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
