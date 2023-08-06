function component(path) {
  const options = {
    moduleCache: {
      vue: Vue,
    },
    getFile(url) {
      return fetch(url).then((response) =>
        response.ok ? response.text() : Promise.reject(response)
      );
    },
    addStyle(styleStr) {
      const style = document.createElement("style");
      style.textContent = styleStr;
      const ref = document.head.getElementsByTagName("style")[0] || null;
      document.head.insertBefore(style, ref);
    },
    log(type, ...args) {
      console.log(type, ...args);
    },
  };
  const { loadModule } = window["vue3-sfc-loader"];
  return Vue.defineAsyncComponent(() => loadModule(path, options));
}

function formatItem(item) {
  let result = {};
  for (key in item) {
    // console.log(item[key])
    result[key] = isJSON(item[key])
      ? this.formatItem(JSON.parse(item[key]))
      : item[key];
    // result[key] = item[key]
  }
  return result;
}

function isJSON(str) {
  if (str.length <= 0) return false;
  if (typeof str !== "string") return false;
  /*
    return /^[\],:{}\s]*$/.test(str.replace(/\\["\\\/bfnrtu]/g, '@').
        replace(/"[^"\\\n\r]*"|true|false|null|-?\d (?:\.\d*)?(?:[eE][\-]?\d )?/g, ']').
        replace(/(?:^|:|,)(?:\s*\[) /g, ''))
    */
  /*
    console.log(1, str.replace(/\\["\\\/bfnrtu]/g, '@'))
    console.log(2, str.replace(/\\["\\\/bfnrtu]/g, '@').replace(/"[^"\\\n\r]*"|true|false|null|-?\d(?:\.\d*)?(?:[eE][\-]?\d)?/g, ''))
    console.log(3, str.replace(/\\["\\\/bfnrtu]/g, '@').replace(/"[^"\\\n\r]*"|true|false|null|-?\d(?:\.\d*)?(?:[eE][\-]?\d)?/g, '').replace(/(?:^|:|,)(?:\s*\[) /g, ''))
    */
  str = str
    .replace(/\\["\\\/bfnrtu]/g, "@")
    .replace(
      /"[^"\\\n\r]*"|true|false|null|-?\d(?:\.\d*)?(?:[eE][\-]?\d)?/g,
      ""
    )
    .replace(/(?:^|:|,)(?:\s*\[) /g, "");
  // console.log(str.match(/^[\[\{].*[\}\]]$/))
  return /^[\[\{].*[\}\]]$/.test(str);
}

function get(
  url,
  params,
  opt = {
    _success: undefined,
    _error: undefined,
    _before: undefined,
    _final: undefined,
  }
) {
  opt["_before"] && opt["_before"]();
  axios
    .get(url, {
      params: params,
    })
    .then((response) => {
      if (response.status === 200) {
        let data = response.data;
        if (data["code"] === 0) {
          opt["_success"] && opt["_success"](data);
        } else {
          console.log("FAILED: " + data["msg"]);
          opt["_error"] && opt["_error"](data);
        }
      }
    })
    .catch(function (error) {
      console.log(error);
      alert(error);
      opt["_error"] && opt["_error"]({ msg: error });
    })
    .finally(function () {
      opt["_final"] && opt["_final"]();
    });
}

function post(
  url,
  params,
  opt = {
    _success: undefined,
    _error: undefined,
    _before: undefined,
    _final: undefined,
  }
) {
  opt["_before"] && opt["_before"]();
  axios
    .post(url, params)
    .then((response) => {
      if (response.status === 200) {
        let data = response.data;
        if (data["code"] === 0) {
          opt["_success"] && opt["_success"](data);
        } else if (data["code"] === -1) {
          console.log("FAILED: " + data["msg"]);
          opt["_error"] && opt["_error"](data);
        } else {
          download(response)
        }
      }
    })
    .catch(function (error) {
      console.log(error);
      alert(error);
      opt["_error"] && opt["_error"]({ msg: error });
    })
    .finally(function () {
      opt["_final"] && opt["_final"]();
    });
}

function download(response) {
  let data = response.data;
  console.log(data.length);
  let fileURL = window.URL.createObjectURL(new Blob([data]));
  let fileLink = document.createElement("a");
  
  fileLink.href = fileURL;
  let name = "back.tar.gz";
  console.log(response.headers["content-disposition"].split("=")[1]);
  const desc = response.headers["content-disposition"];
  if (desc && desc.includes("=")) {
    name = desc.split("=")[1];
  }
  fileLink.setAttribute("download", name);
  document.body.appendChild(fileLink);

  fileLink.click();
  document.body.removeChild(fileLink);
}

function log(str, flag) {
  console.log(JSON.stringify(str), flag);
}

function alert_(text) {
  let liveToast = document.querySelector("#liveToast");
  if (liveToast) {
    liveToast.querySelector("strong").innerText = text;
    $("#liveToast").toast("show");
  } else {
    window.alert(text);
  }
}

function alert(msg) {
  layer.alert(msg, {
    time: 5 * 1000,
    success: function (layero, index) {
      var timeNum = this.time / 1000,
        setText = function (start) {
          layer.title((start ? timeNum : --timeNum) + " 秒后关闭", index);
        };
      setText(!0);
      this.timer = setInterval(setText, 1000);
      if (timeNum <= 0) clearInterval(this.timer);
    },
    end: function () {
      clearInterval(this.timer);
    },
  });
}

function prefix(num, n = 2, s = 0) {
  if (typeof num !== "number") num = Number(num);
  if (isNaN(num)) num = "";
  return (Array(n).join(s) + num).slice(-n);
}

let ua = navigator.userAgent.toLowerCase();
let isFirefox = ua.indexOf("firefox") >= 0;
let isChrome = ua.indexOf("chrome") >= 0;
let isOpera = ua.indexOf("opera") >= 0;
let isIE = ua.indexOf("msie") >= 0;
