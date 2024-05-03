# Mixxx m3u loader

Tiny helper to load a m3u as a playlist on Mixxx, the normal way to do that involves having to manually delete the playlist then having to reload it from disk which is a PITA when having to maintain several

The script doesn't require the mixxx library to be up to date but won't add the tracks to the playlist if they don't exist in its index.

So it might be better to make sure to update mixxx cache before executing the script.

## Installation 

The script requires python 3.9+, no extra dependencies

```
make install
```

## Usage

```
usage: mixxx-m3u-loader [-h] --mix-db MIX_DB --m3u M3U [-v]

options:
  -h, --help       show this help message and exit
  --mix-db MIX_DB  The mixxx DB path, typically on linux $HOME/.mixxx/mixxxdb.sqlite
  --m3u M3U        Path of the m3u to add as a mixxx tracklist
  -v, --verbose    Control script verbosity
```

The script currently deletes a playlist and the associated PlaylistTracks but the song analysis lives in another table of the SQL db so it's not an issue, if the m3u becomes too long it could be worth optimizing later though.
