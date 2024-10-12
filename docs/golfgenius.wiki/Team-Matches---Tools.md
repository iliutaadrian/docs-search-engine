Ability to recreate rounds when missing:

```
# The ID of the Interclub::Championship
x = 106
Interclub::Championship.find(x).sections.each do |s|
  schedule_ids = s.schedules.where(round_id: nil).collect(&:id)
  Interclubs::GenerateStructure.new(x, false, false, [], schedule_ids).sync_schedules
  Interclubs::SyncTournaments.new(x, true, s.id, [], schedule_ids).sync_schedules
end
```