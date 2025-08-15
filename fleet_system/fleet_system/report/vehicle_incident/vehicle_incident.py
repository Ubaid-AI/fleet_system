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
	data = get_vehicle_incident_data(filters)
	# chart = get_chart_data(data, filters)
	# report_summary = get_summary_report(data,filters)

	return columns, data, None , None
	# , report_summary
	# , chart

def get_columns():
	return [
		{
			'fieldname': 'vehicle',
			'fieldtype': 'Link',
			'label': _('Vehicle'),
			'options': 'Vehicle',
			'width': 100
		},
		{
			'fieldname': 'Employee',
			'fieldtype': 'Link',
			'label': _('Employee'),
			'width': 70
		},
		{
			'fieldname': 'incident_date',
			'fieldtype': 'Data',
			'label': _('Incident Date'),
			'width': 70
		},
		{
			'fieldname': 'projectvisit_purpose',
			'fieldtype': 'Data',
			'label': _('Project/Visit Purpose'),
			'width': 70
		},
		
		{
			'fieldname': 'location',
			'fieldtype': 'Data',
			'label': _('Location'),
			'width': 70
		},
		{
			'fieldname': 'incident_type',
			'fieldtype': 'Data',
			'label': _('Accident Type'),
			'width': 70
		}		
		
	]


def get_vehicle_incident_data(filters):
	
	# start_date, end_date = get_period_dates(filters)
	conditions, values = get_conditions(filters)

	data = frappe.db.sql("""
		SELECT  vehicle, incident_type, employee_no, incident_date, location, projectvisit_purpose
		FROM `tabVehicle Incident`
		WHERE
			 incident_date between %(start_date)s and %(end_date)s 
			{0}
		ORDER BY incident_date""".format(conditions), values, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ''

	# start_date, end_date = get_period_dates(filters)
	
	values = {
		'start_date': filters.from_date,
		'end_date': filters.to_date
	}

	if filters.employee:
		conditions += ' and employee_no = %(employee_no)s'
		values['employee_no'] = filters.employee

	if filters.license_plate:
		conditions += ' and vehicle = %(vehicle)s'
		values['vehicle'] = filters.license_plate
	
	if filters.accident_type:
		conditions += ' and accident_type = %(accident_type)s'
		values['accident_type'] = filters.accident_type

	return conditions, values

