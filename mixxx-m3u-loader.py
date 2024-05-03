#!/usr/bin/env python3

import sqlite3
import datetime
import argparse
import logging
from pathlib import Path

logger = logging.getLogger()

TRACK_NOT_FOUND = -1


def read_locations(m3u):
    with open(m3u, "r") as file:
        for line in file.readlines():
            if not line.startswith("#"):
                yield str(line).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mix-db",
        required=True,
        type=str,
        help="The mixxx DB path, typically on linux $HOME/.mixxx/mixxxdb.sqlite",
    )
    parser.add_argument(
        "--m3u",
        required=True,
        type=str,
        help="Path of the m3u to add as a mixxx tracklist",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Control script verbosity"
    )

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARN)

    conn = sqlite3.connect(args.mix_db)

    def sql(request):
        logger.debug(f"SQL => {request}")
        return conn.execute(request)

    m3u = args.m3u
    playlist_name = Path(m3u).stem

    def find_location(path: str) -> int:
        res = sql(
            f"SELECT id FROM track_locations WHERE location = '{path}'"
        ).fetchone()
        if not res:
            return TRACK_NOT_FOUND
        return res[0]

    locations = list(
        filter(lambda a: a != TRACK_NOT_FOUND, map(find_location, read_locations(m3u)))
    )

    def find_track_id(location: int) -> int:
        res = sql(f"SELECT id FROM library WHERE location = {location}").fetchone()
        return res[0]

    tracks_id = list(map(find_track_id, locations))

    playlist_id = sql(
        f"SELECT id FROM Playlists WHERE name = '{playlist_name}'"
    ).fetchone()
    if not playlist_id:
        max_id = sql(f"SELECT MAX(id) FROM Playlists").fetchone()
        if not max_id:
            max_id = 1
        else:
            max_id = max_id[0] + 1
        playlist_id = max_id
    else:
        # Delete playlist and all tracks associated
        playlist_id = playlist_id[0]
        sql(f"DELETE FROM PlaylistTracks WHERE playlist_id = {playlist_id}")
        sql(f"DELETE FROM Playlists WHERE id = {playlist_id}")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    position = 0

    # Generate the tracklist
    for t in tracks_id:
        sql(
            f"INSERT INTO PlaylistTracks (playlist_id, track_id, position, pl_datetime_added) VALUES ({playlist_id}, {t}, {position}, '{now}')"
        )

    sql(
        f"INSERT INTO Playlists (id, name, position, date_created, date_modified, hidden, locked) VALUES ({playlist_id}, '{playlist_name}', {playlist_id}, '{now}', '{now}', 0, 0)"
    )

    conn.commit()


if __name__ == "__main__":
    main()
