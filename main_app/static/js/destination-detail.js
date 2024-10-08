const image = document.getElementById('destination-image')
const overlay = document.getElementById('screen-overlay')

image.addEventListener('click', () => {
  overlay.style.display = 'flex'
})

overlay.addEventListener('click', () => {
  overlay.style.display = 'none'
})
