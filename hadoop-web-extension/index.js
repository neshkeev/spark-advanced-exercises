const url = new URL(window.location.href)

const domain = url.hostname

function main() {
  document.querySelectorAll('a[href*="//worker-"]').
    forEach(e => {
      const newPort = e.getAttribute("href")
                    .replace(/([0-9]):/, "$1")
                    .replace(/^\/\//, url.protocol + "//")
                    .replace("worker-", domain + ":")
      const newUrl = new URL(newPort)
      e.setAttribute("href", newUrl.toString())
    })
  document.querySelectorAll('a[href^="http://resourcemanager"]').
    forEach(e => {
      const newUrl = e.getAttribute("href").replaceAll("http://resourcemanager", domain)
      e.setAttribute("href", newUrl)
    })
  document.querySelectorAll('a[href^="http://namenode"]').
    forEach(e => {
      const newUrl = e.getAttribute("href").replaceAll("http://namenode", domain)
      e.setAttribute("href", newUrl)
    })
}

if (url.protocol == "http:" && url.port) {
  main()
}
