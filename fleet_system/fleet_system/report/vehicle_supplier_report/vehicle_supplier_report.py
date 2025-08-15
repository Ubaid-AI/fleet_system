# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals


import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns(filters=filters)
	data = get_data(filters)
	return columns, data

	
@frappe.whitelist()
def get_data(filters = None):
	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date cannot be greater than To Date"))
	conditions = get_filter_conditions(filters)
	start_date, end_date = filters.from_date, filters.to_date
	values = {
		'start_date': start_date,
		'end_date': end_date
	}

	data = frappe.db.sql("""
		SELECT DISTINCT vl.invoice , vl.license_plate,v.employee_name, vl.make, vl.supplier, vl.fuel_qty, vl.price, vl.total_price, vl.date, vl.name as log_name
		from `tabVehicle Log` vl, `tabFleet Vehicle` v, `tabVehicle Service` s
		WHERE v.name = vl.license_plate and 
		vl.date between %(start_date)s and %(end_date)s
		and vl.docstatus = 1 {0}
		ORDER BY vl.date""".format(conditions), values,  as_dict=1)
	
	for row in data:
		row['service_expense'], supplier = get_service_expense(row['log_name'])
		if not row['total_price']:
			row['total_price'] = 0
		if not row['service_expense']:
			row['service_expense'] = 0
		if not row['supplier']:
			row['supplier'] = supplier
		row['total'] = row['total_price'] + row['service_expense']

	if data:
		data[-1]['fuel_qty'] = round(data[-1]['fuel_qty'], 2)
	return data


def get_service_expense(logname):
	expense_amount = frappe.db.sql("""
		SELECT sum(expense_amount), service.supplier
		FROM
			`tabVehicle Log` log, `tabVehicle Service` service
		WHERE
			service.parent=log.name and log.name=%s
	""", logname)

	return expense_amount[0][0] if expense_amount else 0.0, expense_amount[0][1]


def get_columns(filters=None):
	columns = [
			{
				"label": _("Slip No"),
				"fieldname": "invoice",
				"fieldtype": "Data",
				"width": 100
			},
			{
				"label": _("Vehicle No"),
				"fieldname": "license_plate",
				"fieldtype": "Link",
				"options": "Vehicle",
				"width": 125
			},
			
			{
				"label": _("Employee Name"),
				"fieldname": "employee_name",
				"fieldtype": "Data",
				"width": 100
			},
			{
				"label": _("Make"),
				"fieldname": "make",
				"fieldtype": "Data",
				"width": 100
			},
			{
				"label": _("Supplier"),
				"fieldname": "supplier",
				"fieldtype": "Data",
				"width": 100
			},
			{
				"label": _("Date"),
				"fieldname": "date",
				"fieldtype": "date",
				"width": 175
			},
			{
				"label": _("Qty"),
				"fieldname": "fuel_qty",
				"fieldtype": "Data",
				"width": 120
			},
			{
				"label": _("Rate"),
				"fieldname": "price",
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"label": _("Gross Amount (Petrol)"),
				"fieldname": "total_price",
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"label": _("Gross Amount (Service)"),
				"fieldname": "service_expense",
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"label": _("Total"),
				"fieldname": "total",
				"fieldtype": "Currency",
				"width": 120
			},
	]
	return columns


def get_filter_conditions(filters):
	conditions = ""
	
	
	if filters.get("license_plate"):
		conditions += " and vl.license_plate = '%s' " % (filters.get("license_plate"))

	if filters.get("supplier"):
		conditions += " and vl.supplier = '%s' " % (filters.get("supplier").replace("'","''"))

	# if filters.get("warehouse"):
	# 	conditions += " and warehouse = '%s' " % (filters.get("warehouse"))
	
	if filters.get("invoice"):
		conditions += " and vl.invoice = '%s' " % (filters.get("invoice"))

	# if filters.get("serial_no"):
	# 	conditions += " and serial_no = '%s' " % (filters.get("serial_no"))

	# if filters.get("item_code"):
	# 	conditions += " and item_code = '%s' " % (filters.get("item_code"))
	
	# if filters.get("status"):
	# 	conditions += " and status = '%s' " % (filters.get("status"))

	# if filters.get("area"):
	# 	conditions += " and area  = '%s' " % (filters.get("area"))

	return conditions