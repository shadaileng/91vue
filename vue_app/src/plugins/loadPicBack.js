import {DEFAULT_URL} from '@/constant'

const loadPicBack = {
  install (app, options) {
    app.directive('loadback', {
        mounted: (el, binding) => {
            load(el, binding)
        },
        updated: (el, binding) => {
            if (el.style.backgroundImage.indexOf(binding.value.val1) < 0 || el.style.backgroundImage.indexOf(binding.value.val2) < 0) return
            load(el, binding)
        },
    })
  }
}

const load = (el, binding) => {
    el.style.width = "100%"
    // el.setAttribute('src', DEFAULT_URL)
    el.style.backgroundImage = `url(${DEFAULT_URL})`
    // console.log(binding.value)
    const src = binding.value.val1
    const src1 = binding.value.val2
    loadImage(src).then(() => {
        // el.setAttribute('src', src)
        el.style.backgroundImage = `url(${src})`
        el.style.width = binding.value.width || "100%"
        el.style.height = binding.value.height || "100%"
    }).catch((e) => {
        if (src1) {
            loadImage(src1).then(() => {
                // el.setAttribute('src', src)
                el.style.backgroundImage = `url(${src1})`
                el.style.width = binding.value.width || "100%"
                el.style.height = binding.value.height || "100%"
            }).catch((e) => {
                console.warn(`load failed with src image(${src1}) and the error msg is ${e.message}`)
            })
        } else {
            // console.warn(`load failed with src image(${src}) and the error msg is ${e.message}`)
        }
    })
}

export default loadPicBack

function loadImage (src) {
  return new Promise((resolve, reject) => {
    const image = new Image()
    // timeout
    image.onload = function () {
        resolve()
        dispose()
    }

    image.onerror = function (e) {
        reject(e)
        dispose()
    }

    image.src = src

    function dispose () {
        image.onload = image.onerror = null
    }
  })
}