/* xlsx.js (C) 2013-present SheetJS -- http://sheetjs.com */
/* uncomment the next line for encoding support */
importScripts('plugins/cpexcel.js');
importScripts('plugins/jszip.js');
importScripts('plugins/xlsx.js');
postMessage({ t: "ready" });

onmessage = function(oEvent) {
    var v;
    try {
        v = XLSX.read(oEvent.data.d, { type: oEvent.data.b });
        postMessage({ t: "xlsx", d: JSON.stringify(v) });
    } catch (e) { postMessage({ t: "e", d: e.stack || e }); }
};