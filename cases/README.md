# 3D case library

Public pages: `/cases/` (library) and `/cases/view.html?c=<slug>` (viewer).
The "3D cases" nav link and the banner on the home page appear automatically once `cases.json` has at least one entry.

Before publishing any file: open it and confirm it has no patient name, date of birth, clinic or doctor name (exocad HTML exports can carry the project name in the page title/metadata).

## Add an exocad HTML export
Put the file in `files/<slug>.html` and add to `cases.json`:
```json
{"slug":"implant-crown-36","title":"Implant crown with custom abutment","category":"single",
 "teeth":"36","details":["Zirconia","Ti-base"],"thumb":"../img/case12.jpg",
 "type":"exocad","file":"files/implant-crown-36.html"}
```

## Add STL / PLY meshes
Put parts in `files/<slug>/` and use `"type":"mesh"`:
```json
{"slug":"bridge-14-16","title":"3-unit bridge 14–16","category":"bridge","teeth":"14–16",
 "type":"mesh","up":"z","startView":"front",
 "parts":[{"name":"Bridge","file":"files/bridge-14-16/bridge.stl","color":"#efe9dd"},
          {"name":"Abutment","file":"files/bridge-14-16/abut.stl","color":"#b8bec6","metal":true},
          {"name":"Model","file":"files/bridge-14-16/model.stl","color":"#c9b39b","opacity":0.85}]}
```
`category`: single | bridge | full. `up`: axis pointing occlusal (`z` for exocad exports, `y` otherwise).
Optional per part: `opacity`, `visible:false`, `metal:true`, `roughness`, `clearcoat`.

three.js r160 is vendored in `lib/` (MIT, see `lib/THREE-LICENSE`).
