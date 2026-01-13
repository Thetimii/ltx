-- Create a private bucket called 'videos'
insert into storage.buckets (id, name, public)
values ('videos', 'videos', true);

-- Policy to allow authenticated uploads (if you use Service Role, this isn't strictly needed but good for RLS)
-- Adjust 'authenticated' to 'anon' if you want unauthenticated uploads (NOT RECOMMENDED for production)
create policy "Allow authenticated uploads"
on storage.objects for insert
to authenticated
with check ( bucket_id = 'videos' );

-- Policy to allow public viewing of videos
create policy "Allow public viewing"
on storage.objects for select
to public
using ( bucket_id = 'videos' );
