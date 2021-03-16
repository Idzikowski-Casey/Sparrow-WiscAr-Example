import aboutText from "./about-lab.md";
import { Markdown } from "@macrostrat/ui-components";
import h from "@macrostrat/hyper";
import { StepHeatingChart } from "plugins/step-heating";
import { PlateauAgesComponent } from "plugins/plateau-ages";
import { GLMap } from "plugins/gl-map";
import { CanvasDownloader } from "./custom-components";
import { Tab, Tabs } from "sparrow/components/tab-panel";
import { SampleMap } from "../plugins/globe";

export default {
  siteTitle: "WiscAr",
  landingText: h(Markdown, { src: aboutText }),
  sessionDetail: (props) => {
    const { defaultContent, ...rest } = props;
    return h(
      Tabs,
      {
        id: "sessionDetailTabs",
      },
      [
        h(
          Tab,
          { id: "stepHeating", panel: h(StepHeatingChart, rest) },
          "Step heating chart"
        ),
        h(
          Tab,
          { id: "analysisDetails", panel: h(defaultContent, rest) },
          "Analysis details"
        ),
      ]
    );
  },
  landingGraphic: (props) => {
    const { defaultContent, ...rest } = props;
    return h(
      Tabs,
      {
        id: "sessionDetailTabs",
      },
      [
        h(Tab, { id: "sample-map", panel: h(SampleMap) }, "Sample map"),
        h(
          Tab,
          { id: "plateau-ages", panel: h(PlateauAgesComponent) },
          "Plateau ages histogram"
        ),
      ]
    );
  },
  samplePage: (props) => {
    const { defaultContent, ...rest } = props;
    return h(CanvasDownloader, rest);
  },
};
