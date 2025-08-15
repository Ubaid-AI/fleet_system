// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.query_reports["Service Request"] = {
	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},
	onload: function(report) {	
		buttons = document.querySelector('.custom-actions')
		// console.log(buttons)
		
		buttons.classList.remove('hidden-xs')
		buttons.classList.remove('hidden-md')
        // Add a custom button to save the checkbox value
        report.page.add_inner_button(__('Approve'), function() {
			let checked_rows_indexes = report.datatable.rowmanager.getCheckedRows();
			let checked_rows = checked_rows_indexes.map(i => report.data[i]);
			// create empty array which will save name, barcode and itemcode 
			console.log(checked_rows)
			const selected_data = new Array();
			
			// in this loop only specific fields are saved in new arrays NAME, BARCODE, ITEMCODE
			checked_rows.forEach(row=>/* row is an variable inside this loop, in each iteration 
									it's value is dictionary. from this dictionary we are saving required fields*/
				{	// push data as dictionary in new array
					console.log(row.name)

					
					frappe.call('erpnext.fleet_ms.doctype.service_request.service_request.update_approved_status',
					{'status': 'Approved','name': row.name})
					.then(r => {
						alert('Success!');
					});
					// update_approved_status('Approved', row.name);
					console.log(report)
				}	
			)
			frappe.msgprint('Success!');
	
        })
		report.page.add_inner_button(__('Reject'), function() {
            let checked_rows_indexes = report.datatable.rowmanager.getCheckedRows();
			let checked_rows = checked_rows_indexes.map(i => report.data[i]);
			// create empty array which will save name, barcode and itemcode 
			console.log(checked_rows)
			const selected_data = new Array();
			
			// in this loop only specific fields are saved in new arrays NAME, BARCODE, ITEMCODE
			checked_rows.forEach(row=>/* row is an variable inside this loop, in each iteration 
									it's value is dictionary. from this dictionary we are saving required fields*/
				{	// push data as dictionary in new array
					console.log(row.name)
					frappe.call('erpnext.fleet_ms.doctype.service_request.service_request.update_approved_status',{'status': 'Rejected','name': row.name})
					.then(r => {
						alert('Success!');
					});
					console.log(report)
				}	
			)
			frappe.msgprint('Success!');
        });
    },
	
	"filters": [
		{
			"fieldname": "license_plate",
			"label": __("Vehicle"),
			"fieldtype": "Link",
			"options": "Fleet Vehicle"
		}
	]
};
