/**
 *  Light Switch @version v0.1.4
 */

function dark_light_switcher() {
    let dark_stylesheet = document.getElementsByName('dark_stylesheet')[0]
    if (dark_stylesheet.value === 0) {
        dark_stylesheet.value = 1
        dark_stylesheet.href = '/'
    } else {
        dark_stylesheet.value = 0
        dark_stylesheet.href = '/static/css/bootstrap-night.min.css'
    }
}
