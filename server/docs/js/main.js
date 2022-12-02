var search = document.getElementById('search');
    searchError = document.getElementById('searchError');
    methods = document.getElementById('methods');
    links = document.getElementById('links');
    errors = document.getElementById('errors');
    errorLinks = document.getElementById('errorLinks');
    methodsContainer = document.getElementById('methodsContainer');
    errorsContainer = document.getElementById('errorsContainer');

if (errorsContainer != null) {
    errorsContainer.style.display = 'none';
    searchError.addEventListener('input', () => {
        let searched = searchError.value.toLowerCase();
        if (errors == null || errorLinks == null)
            return;
        [...errors.children].forEach(e =>  {
          if (e.outerHTML.toLowerCase().includes(searched))
              e.style.display = 'flex';
          else
              e.style.display = 'none';
        });
        [...errorLinks.children].forEach(e =>  {
          if (e.outerHTML.toLowerCase().includes(searched))
              e.style.display = 'flex';
          else
              e.style.display = 'none';
        });
    });
}


search.addEventListener('input', () => {
    let searched = search.value.toLowerCase();
    if (methods == null || links == null)
        return;
    [...methods.children].forEach(e =>  {
    if (e.outerHTML.toLowerCase().includes(searched))
        e.style.display = 'flex';
    else
        e.style.display = 'none';
    });
    [...links.children].forEach(e =>  {
    if (e.outerHTML.toLowerCase().includes(searched))
        e.style.display = 'flex';
    else
        e.style.display = 'none';
    });
});


function goTo(container) {
    switch (container) {
        case 'errors':
            errorsContainer.style.display = 'flex';
            methodsContainer.style.display = 'none';
            break;
        case 'methods':
            errorsContainer.style.display = 'none';
            methodsContainer.style.display = 'flex';
            break;
    }
}

async function sendReq(urlParams, jsonBody, id, method, api_url) {
  var path = method.split(' ')[1]

  console.log(path)
  for (key in urlParams) {
    console.log(key)
    if (path.includes(`{${key}}`)) {
        path = path.replace(`{${key}}`, urlParams[key])
        delete urlParams[key]
    }
  }
  console.log(path)

  const response = await fetch(
    `${api_url}${path}?` + new URLSearchParams(urlParams), {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: method.split(' ')[0],
      json: jsonBody
    }
  )
  var elem = document.getElementById(id)
  elem.innerHTML = method + '\n\n' + JSON.stringify(await response.json(), null, 2)
  hljs.highlightElement(elem)
}
