-- LogicQuest: one progress document per user, merged client-side.
create table if not exists public.user_progress (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  state      jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.user_progress enable row level security;

create policy "read own progress" on public.user_progress
  for select using (auth.uid() = user_id);

create policy "insert own progress" on public.user_progress
  for insert with check (auth.uid() = user_id);

create policy "update own progress" on public.user_progress
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Optional leaderboard-friendly view (XP only, no code).
create or replace view public.progress_summary
with (security_invoker = true) as
select user_id,
       coalesce((state ->> 'xp')::int, 0) as xp,
       updated_at
from public.user_progress;
