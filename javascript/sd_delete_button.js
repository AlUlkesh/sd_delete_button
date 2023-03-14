function txt2img_sdelb_hide() {
    const txt2img_sdelb_delete_info = gradioApp().getElementById('txt2img_sdelb_delete_info')
    txt2img_sdelb_delete_info.style.display = 'none'
}

function img2img_sdelb_hide() {
    const img2img_sdelb_delete_info = gradioApp().getElementById('img2img_sdelb_delete_info')
    img2img_sdelb_delete_info.style.display = 'none'
}

function txt2img_sdelb_addEventListener() {
    const txt2img_generate = gradioApp().getElementById('txt2img_generate')
    txt2img_generate.removeEventListener('click', txt2img_sdelb_hide)
    txt2img_generate.addEventListener('click', txt2img_sdelb_hide)
    const txt2img_sdelb_delete_info = gradioApp().getElementById('txt2img_sdelb_delete_info')
    txt2img_sdelb_delete_info.style.display = ''
}

function img2img_sdelb_addEventListener() {
    const img2img_generate = gradioApp().getElementById('img2img_generate')
    img2img_generate.removeEventListener('click', img2img_sdelb_hide)
    img2img_generate.addEventListener('click', img2img_sdelb_hide)
    const img2img_sdelb_delete_info = gradioApp().getElementById('img2img_sdelb_delete_info')
    img2img_sdelb_delete_info.style.display = ''
}
