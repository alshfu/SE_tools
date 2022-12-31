function createNewInputElement(name = '') {
    var div_element = document.createElement("div")
    div_element.classList.add("col-auto")
    div_element.classList.add("me-2")
    div_element.classList.add("ref_input")

    var input_element = document.createElement("input");
    input_element.classList.add("form-control")
    input_element.type = "text"
    input_element.name = name

    div_element.appendChild(input_element)
    return div_element
}

function addNewReference() {
    var plus_btn = event.target
    var parent_element = plus_btn.parentElement.parentElement.parentElement;
    if (parent_element.id != "settings_table") {
        let id_of_parent_element = parent_element.id
        let last_input = parent_element.getElementsByClassName('ref_input')[parent_element.getElementsByClassName('ref_input').length - 1]
        last_input
        console.log(last_input)
        let new_input = createNewInputElement(name= last_input.name)
       last_input.after(new_input)
    }


}