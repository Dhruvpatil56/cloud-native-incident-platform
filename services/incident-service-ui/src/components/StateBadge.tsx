import type { IncidentState } from "../types/incident";
export function StateBadge({ state }: { state: IncidentState }) {
  if (!state) return null;
  return (
    <span className={`state-badge ${state.toLowerCase()}`}>
      {state}
    </span>
  );
}
