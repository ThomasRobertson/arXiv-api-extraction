import connect_to_arxiv
import fill_data_base


def main():
    harvester = connect_to_arxiv.ArXivHarvester()
    record = next(harvester.next_record())
    first_harvest_first_record = harvester.get_record_header(record)
    for i, record in enumerate(harvester.next_record(), 0):
        if i == 999:
            break
    first_harvest_last_record = harvester.get_record_header(record)
    record = next(harvester.next_record())
    second_harvest_first_record = harvester.get_record_header(record)

    # checking for empty dict
    assert bool(first_harvest_first_record) is True
    assert bool(first_harvest_last_record) is True
    assert bool(second_harvest_first_record) is True

    assert first_harvest_first_record != first_harvest_last_record
    assert first_harvest_first_record != second_harvest_first_record


if __name__ == "__main__":
    main()
