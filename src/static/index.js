const btnsConfirm = document.querySelectorAll("#btn-borrar")

if (btnsConfirm.length) {
    for (const btn of btnsConfirm) {
        btn.addEventListener("click", Event => {
            console.log(Event)
            const resp = confirm("Esta opción no tiene marcha atrás. ¿Confirma?")
            if (!resp) {
                Event.preventDefault()
            }
        })
    }
}
