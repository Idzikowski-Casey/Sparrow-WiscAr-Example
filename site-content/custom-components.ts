import React, { useEffect, useRef } from "react";
import html2canvas from "html2canvas";
import { Button } from "@blueprintjs/core";
import { hyperStyled } from "@macrostrat/hyper";
//@ts-ignore
import styles from "./module.styl";

const h = hyperStyled(styles);

export function CanvasDownloader(props) {
  if (!props) return null;

  const { name } = props.data;
  console.log(name);

  const onClick = () => {
    console.log("The Door is Opened");
    const c = document.getElementById("hal");
    html2canvas(c).then(function(canvas) {
      const dataURI = canvas.toDataURL();
      const a = document.createElement("a");
      document.body.append(a);
      a.href = dataURI;
      a.download = `${name}-mount.png`;
      a.click();
      document.body.removeChild(a);
    });
  };

  return h("div", [
    h("div.canvas", { id: "hal" }, [
      h("div.label-top", [
        h("h1", "Open the pod bay doors, please, HAL"),
        h("h3", `Samlpe Name: ${name}`),
      ]),
      h("div.label-bottom", [
        "Cast in Epoxy, Cut on Lines",
        h("hr.dashed"),
        "Standard",
        h("hr.dashed"),
        `Sample # (${name})`,
        h("hr.dashed"),
        "Museum Name",
      ]),
    ]),
    h(Button, { intent: "success", onClick }, ["Open the Doors for David"]),
  ]);
}
