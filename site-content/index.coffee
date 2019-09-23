import aboutText from './index.md'
import {Markdown} from '@macrostrat/ui-components'
import h from '@macrostrat/hyper'
import {StepHeatingChart} from 'plugins/step-heating'
import {PlateauAgesComponent} from 'plugins/plateau-ages'
import {GLMap} from 'plugins/gl-map'
import {Tab, Tabs} from 'sparrow/components/tab-panel'

export default {
  siteTitle: "WiscAr"
  landingText: h Markdown, {src: aboutText}
  sessionDetail: (props)=>
    {defaultContent, rest...} = props
    h Tabs, {
      id: 'sessionDetailTabs'
    }, [
      h Tab, {id: 'stepHeating', panel: h(StepHeatingChart, rest)}, "Step heating chart"
      h Tab, {id: 'analysisDetails', panel: h(defaultContent, rest)}, "Analysis details"
    ]
  landingGraphic: (props)=>
    {defaultContent, rest...} = props
    h Tabs, {
      id: 'sessionDetailTabs'
    }, [
      h Tab, {id: 'sample-map', panel:  defaultContent}, "Sample map"
      h Tab, {id: 'plateau-ages', panel: h(PlateauAgesComponent)}, "Plateau ages histogram"
    ]
}
