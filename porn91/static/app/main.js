function assign(path) {
    let _prefix = (path.indexOf('?') >= 0 ? path.split('?')[0] : path).split('/').slice(-1)
    if (_prefix == prefix) {
        params = ''
        if (path.indexOf('?') >= 0) {
            params = path.slice(path.indexOf('?') + 1)
            path = path.slice(0, path.indexOf('?'))
        }
        let flags = ['mode', 'index', 'pagesize', 'status', 'uname', 'name']
        for (index in flags) {
            let flag = flags[index]
            let value = get_cookie(flag)
            if ((params.indexOf('&' + flag + '=') == -1 && !params.startsWith(flag + '=')) && value && value.length > 0) {
                if (params.length > 0) {
                    params += '&'
                }
                if (value.indexOf('&') >= 0) {
                    value.replaceAll('&', '%26')
                }
                params += (flag + '=' + value)
            }
        }
        path += '?' + params
    }
    path = path.replace('+', '%2B')
    path = path.replace(' ', '%20')

    location.assign(path)
}
querySelector('#mode').addEventListener('click', function (event) {
    if (querySelector('#mode').checked) {
        assign(prefix + '?path=' + cur_path + '&mode=grid')
    } else {
        assign(prefix + '?path=' + cur_path + '&mode=list')
    }
}, false)
querySelector('main').addEventListener('click', () => {
    $('#popupRC').css({ display: 'none' });
}, false)
