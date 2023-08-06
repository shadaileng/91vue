import {DEFAULT_URL} from '@/constant'

const loadPicPlugin = {
  install (app, options) {
    app.directive('loadPicPlugin', {
      mounted: (el, binding) => {
            el.style.width = "50%"
            el.setAttribute('src', DEFAULT_URL)
            const src = binding.value
            loadImage(src).then(() => {
                el.setAttribute('src', src)
                el.style.width = "100%"
            }).catch((e) => {
                console.warn(`load failed with src image(${src}) and the error msg is ${e.message}`)
            })
      },
      updated: (el, binding) => {
            if (el.src === binding.value) return
            el.style.width = "50%"
            el.setAttribute('src', DEFAULT_URL)
            const src = binding.value
            loadImage(src).then(() => {
                el.setAttribute('src', src)
                el.style.width = "100%"
            }).catch((e) => {
                console.warn(`load failed with src image(${src}) and the error msg is ${e.message}`)
            })
      },
    })
  }
}
export default loadPicPlugin

function loadImage (src) {
  return new Promise((resolve, reject) => {
    const image = new Image()

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