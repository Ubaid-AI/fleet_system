// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Driver"] = {
	"filters": [

		// {
		// 	"fieldname": "from_date",
		// 	"label": __("From Date"),
		// 	"fieldtype": "Date",
		// 	// "reqd": 1,
		// 	// "depends_on": "eval: doc.filter_based_on == 'Date Range'",

		// 	"default": frappe.datetime.add_months(frappe.datetime.nowdate(), -12)
		// },
		// {
		// 	"fieldname": "to_date",
		// 	"label": __("To Date"),
		// 	"fieldtype": "Date",
		// 	// "reqd": 1,
		// 	// "depends_on": "eval: doc.filter_based_on == 'Date Range'",
		// 	"default": frappe.datetime.add_months(frappe.datetime.nowdate(), +24),
		// 	"description":"to expiry date"
		// },
		{
			"fieldname": "v.name",
			"label": __("Vehicle"),
			"fieldtype": "Link",
			"options": "Fleet Vehicle"
		},
		{
			"fieldname": "d.name",
			"label": __("Driver"),
			"fieldtype": "Link",
			"options": "Driver"
		}

	]
};


