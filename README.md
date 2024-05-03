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


