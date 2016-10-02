import pytest


@pytest.mark.df_cache_ready
class TestCsvSource:

    def test_df_cache_root(self, csv_sources):
        # Picked these two cause they're somewhat small
        assert type(csv_sources.root.get('claims_perils')).__name__ is 'DataFrame'
        assert type(csv_sources.prepared.get('commission_payments')).__name__ is 'DataFrame'
