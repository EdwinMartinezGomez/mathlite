/**
 * Titlebar — Barra de título con logo y tabs de navegación.
 */
import { S } from '../styles/appStyles'

export default function Titlebar({ activeTab, onTabChange, tabs }) {
  return (
    <div style={S.titlebar}>
      <div style={S.logo}>Math<span style={S.logoSpan}>Lite</span></div>
      <div style={S.subtitle}>intérprete DSL — lenguajes formales 2026-1</div>
      <div style={S.tabs}>
        {tabs.map(tab => (
          <div key={tab.id} style={S.tab(activeTab===tab.id)} onClick={()=>onTabChange(tab.id)}>
            {tab.label}
          </div>
        ))}
      </div>
    </div>
  )
}
