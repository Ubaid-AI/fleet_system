// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Supplier Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.nowdate(), -12)
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.nowdate(), +24),
		},
		{
			"fieldname": "license_plate",
			"label": __("License Plate"),
			"fieldtype": "Link",
			"options": 'Fleet Vehicle',
		},
		{
			"fieldname": "supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": 'Supplier'
		},
		{
			"fieldname": "invoice",
			"label": __("Ref No"),
			"fieldtype": "Data",
		},

	]
};
