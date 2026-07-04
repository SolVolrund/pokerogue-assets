# Contest Assets

Contest-specific graphics should live here so they stay separate from battle, UI, arena, and mystery encounter assets.

Suggested layout:

- `atlases/` - parsed sprite sheets with matching `.png` and `.json` atlas files.
- `backgrounds/` - Contest hall, stage, crowd, and judge backgrounds.
- `ui/` - Contest-only panels, meters, icons, cursors, and labels.
- `debug/` - temporary verification sheets or placement guides.

Runtime loading can use the existing helpers with the `contests` folder, for example:

```ts
this.loadImage("contest_stage", "contests/backgrounds");
this.loadAtlas("contest_ui", "contests/ui");
```

# List of Phases
ContestStartPhase
ContestIntroScorePhase
ContestRoundStartPhase
ContestCommandPhase
ContestAppealPhase
ContestAppealResultPhase
ContestRoundScoringPhase
ContestRoundEndPhase
ContestEndPhase