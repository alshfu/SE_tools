function createNewInputElement(name = '') {
    var input_element = document.createElement("input");
    input_element.classList.add("form-control")
    input_element.type = "text"
    input_element.name = name
    return input_element
}

function addNewTransaction() {
    var plus_btn = event.target
    var parent_element = plus_btn.parentElement.parentElement.parentElement;
    if (parent_element.id != "table_of_verifications") {
        let id_of_parent_element = parent_element.id
        //new row of Transaction
        var tr_of_transaction = document.createElement("tr");
        tr_of_transaction.id = id_of_parent_element
        tr_of_transaction.classList.add("collapse")
        tr_of_transaction.classList.add("show")
        //new transactions data

        var td_of_id = document.createElement("td");
        td_of_id.appendChild(createNewInputElement("id"))
        var td_of_amount = document.createElement("td");
        td_of_amount.appendChild(createNewInputElement("amount"));
        var td_of_account = document.createElement("td");
        td_of_account.appendChild(createNewInputElement("account"));
        var td_of_reference = document.createElement("td");
        td_of_reference.appendChild(createNewInputElement("reference"));

        tr_of_transaction.appendChild(td_of_id)
        tr_of_transaction.appendChild(td_of_amount)
        tr_of_transaction.appendChild(td_of_account)
        tr_of_transaction.appendChild(td_of_reference)

        console.log(parent_element)
        parent_element.after(tr_of_transaction)

    }


}
