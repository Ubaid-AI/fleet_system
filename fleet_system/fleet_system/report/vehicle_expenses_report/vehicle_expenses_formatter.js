frappe.provide("erpnext.vehicle_expenses_report");

erpnext.vehicle_expenses_report = {
	"filters": get_filters(),
	"formatter": function(value, row, column, data, default_formatter) {
		if (data && column.fieldname=="service_expense") {    // account
			value = data.service_expense || value;       // account_name
			column.link_onclick =
				"erpnext.vehicle_expenses_report.open_service_expense(" + JSON.stringify(data) + ")";
			column.is_tree = true;
		}
		value = default_formatter(value, row, column, data);

		if (data && !data.parent_vehicle) {
			value = $(`<span>${value}</span>`);

			var $value = $(value).css("font-weight", "Normal");
			if (data.warn_if_negative && data[column.fieldname] < 0) {
				$value.addClass("text-danger");
			}

			value = $value.wrap("<p></p>").parent().html();
		}

		return value;
	},
	"open_service_expense": function(data) {
		if (!data) return;   //acccount
		var service = $.grep(frappe.query_report.filters, function(e){ return e.df.fieldname == 'service_expense'; })
        console.log(service)
		frappe.route_options = {
            'license_plate':  data.vehicle,
			"employee": frappe.query_report.get_filter_value('employee'),
			"from_date": data.from_date || data.year_start_date,
			"to_date": data.to_date || data.year_end_date,
		};
		console.log(frappe.route_options)
		frappe.set_route("query-report", "Service Expense");
		// frappe.set_filter('Report', 'Vehicle', data.license_plate)

	},
	"tree": true,
	"name_field": "vehicles",
	"parent_field": "parent_vehicle",
	"initial_depth": 3,
	onload: function(report) {
		console.log(`report`)
		console.log(report)
		// dropdown for links to other financial statements
		erpnext.vehicle_expenses_report.filters = get_filters()
		console.log(erpnext.vehicle_expenses_report.filters)
		let fiscal_year = frappe.defaults.get_user_default("fiscal_year")
		let license_plate = frappe.defaults.get_user_default('license_plate')
		frappe.model.with_doc("Fiscal Year", fiscal_year, function(r) {
			var fy = frappe.model.get_doc("Fiscal Year", fiscal_year);
			frappe.query_report.set_filter_value({
				period_start_date: fy.year_start_date,
				period_end_date: fy.year_end_date,
			});
		});

		// frappe.model.with_doc("License Plate", license_plate, function(data) {
		// 	var fy = frappe.model.get_doc("License Plate", license_plate);
		// 	frappe.query_report.set_filter_value({
		// 		license_plate: data.license_plate,
		// 	});
		// });
		const views_menu = report.page.add_custom_button_group(__('Financial Statements'));

		report.page.add_custom_menu_item(views_menu, __("Balance Sheet"), function() {
			var filters = report.get_values();
			frappe.set_route('query-report', 'Balance Sheet', {company: filters.company});
		});

		report.page.add_custom_menu_item(views_menu, __("Profit and Loss"), function() {
			var filters = report.get_values();
			frappe.set_route('query-report', 'Profit and Loss Statement', {company: filters.company});
		});

		report.page.add_custom_menu_item(views_menu, __("Cash Flow Statement"), function() {
			var filters = report.get_values();
			frappe.set_route('query-report', 'Cash Flow', {company: filters.company});
		});
	}
};

function get_filters() {
	let filters = [
		{
			"fieldname": "filter_based_on",
			"label": __("Filter Based On"),
			"fieldtype": "Select",
			"options": ["Fiscal Year", "Date Range"],
			"default": ["Fiscal Year"],
			"reqd": 1
		},
		{
			"fieldname": "fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"depends_on": "eval: doc.filter_based_on == 'Fiscal Year'",
			"reqd": 1
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"depends_on": "eval: doc.filter_based_on == 'Date Range'",
			"default": frappe.datetime.add_months(frappe.datetime.nowdate(), -12)
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"depends_on": "eval: doc.filter_based_on == 'Date Range'",
			"default": frappe.datetime.nowdate()
			
		},
		{
			"fieldname": "license_plate",
			"label": __("License Plate"),
			"fieldtype": "Link",
			"options": "Fleet Vehicle"
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		}
	]

	return filters;
}
