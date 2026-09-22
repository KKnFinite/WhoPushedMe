from uuid import UUID

from who_pushed_me.store import RoundStore


class ResultsCursor:
    def __init__(self, *, net_enabled, route_required, players):
        self.net_enabled = net_enabled
        self.route_required = route_required
        self.players = players
        self.query = ""

    def execute(self, query, params=None):
        self.query = str(query)

    def fetchone(self):
        if "SELECT net_scoring_enabled FROM rounds" in self.query:
            return {"net_scoring_enabled": self.net_enabled}
        if "SELECT count(*) AS required_count" in self.query:
            return {"required_count": self.route_required}
        raise AssertionError(f"unexpected fetchone query: {self.query}")

    def fetchall(self):
        if "SELECT rp.id AS participant_id" in self.query:
            return self.players
        raise AssertionError(f"unexpected fetchall query: {self.query}")


def player_row(
    participant_id,
    name,
    *,
    required=18,
    scores=18,
    total=80,
    state="active",
    tracked_from=1,
    handicap_index=None,
    round_handicap=None,
    handicap_source=None,
):
    return {
        "participant_id": UUID(participant_id),
        "display_name": name,
        "participation_state": state,
        "tracked_from_position": tracked_from,
        "handicap_index": handicap_index,
        "round_handicap": round_handicap,
        "handicap_source": handicap_source,
        "required_count": required,
        "score_count": scores,
        "total_strokes": total,
    }


def results(cursor):
    return RoundStore._round_results_from_cursor(
        cursor,
        UUID("08966fcb-463a-4c27-8da2-5d2f01d8502d"),
        mode="individual",
        hole_count=18,
    )


def test_incomplete_individual_round_has_no_official_placement():
    cursor = ResultsCursor(
        net_enabled=True,
        route_required=18,
        players=[
            player_row(
                "304b4411-bc80-4652-94b3-350ef2501267",
                "Kim",
                scores=18,
                total=80,
                round_handicap=10,
                handicap_source="manual",
            ),
            player_row(
                "404b4411-bc80-4652-94b3-350ef2501267",
                "Pat",
                scores=17,
                total=79,
                round_handicap=12,
                handicap_source="manual",
            ),
        ],
    )

    payload = results(cursor)

    assert payload["complete"] is False
    assert payload["net_official"] is False
    assert all(row["rank"] is None for row in payload["players"])
    assert all(
        row["placement_eligible"] is False
        for row in payload["players"]
    )
    assert all(row["net_rank"] is None for row in payload["players"])


def test_missing_handicap_keeps_gross_official_but_net_pending():
    cursor = ResultsCursor(
        net_enabled=True,
        route_required=18,
        players=[
            player_row(
                "304b4411-bc80-4652-94b3-350ef2501267",
                "Kim",
                total=80,
                round_handicap=10,
                handicap_source="manual",
            ),
            player_row(
                "404b4411-bc80-4652-94b3-350ef2501267",
                "Pat",
                total=82,
            ),
        ],
    )

    payload = results(cursor)
    players = {row["display_name"]: row for row in payload["players"]}

    assert payload["complete"] is True
    assert players["Kim"]["rank"] == 1
    assert players["Pat"]["rank"] == 2
    assert payload["missing_handicaps"] == 1
    assert payload["net_official"] is False
    assert players["Kim"]["net_total_strokes"] == 70
    assert players["Kim"]["net_rank"] is None
    assert players["Pat"]["net_total_strokes"] is None


def test_complete_handicaps_produce_separate_official_net_ranking():
    cursor = ResultsCursor(
        net_enabled=True,
        route_required=18,
        players=[
            player_row(
                "304b4411-bc80-4652-94b3-350ef2501267",
                "Kim",
                total=80,
                round_handicap=8,
                handicap_source="manual",
            ),
            player_row(
                "404b4411-bc80-4652-94b3-350ef2501267",
                "Pat",
                total=82,
                round_handicap=12,
                handicap_source="manual",
            ),
        ],
    )

    payload = results(cursor)
    players = {row["display_name"]: row for row in payload["players"]}

    assert payload["complete"] is True
    assert payload["net_official"] is True
    assert players["Kim"]["rank"] == 1
    assert players["Pat"]["rank"] == 2
    assert players["Kim"]["net_total_strokes"] == 72
    assert players["Pat"]["net_total_strokes"] == 70
    assert players["Kim"]["net_rank"] == 2
    assert players["Pat"]["net_rank"] == 1


def test_partial_player_never_gets_misleading_net_total_or_placement():
    cursor = ResultsCursor(
        net_enabled=True,
        route_required=18,
        players=[
            player_row(
                "304b4411-bc80-4652-94b3-350ef2501267",
                "Kim",
                total=80,
                round_handicap=8,
                handicap_source="manual",
            ),
            player_row(
                "404b4411-bc80-4652-94b3-350ef2501267",
                "Pat",
                required=8,
                scores=8,
                total=38,
                tracked_from=11,
                round_handicap=5,
                handicap_source="manual",
            ),
        ],
    )

    payload = results(cursor)
    players = {row["display_name"]: row for row in payload["players"]}

    assert payload["complete"] is True
    assert players["Pat"]["coverage_state"] == "partial"
    assert players["Pat"]["rank"] is None
    assert players["Pat"]["net_total_strokes"] is None
    assert players["Pat"]["net_rank"] is None
