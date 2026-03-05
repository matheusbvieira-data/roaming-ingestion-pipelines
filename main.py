from src import config
from src.pipelines.national_roaming import NationalRoaming


def main():
    """Main entrypoint."""
    config.main()

    national_roaming_pipeline_inbound = NationalRoaming(
        direction="INB", source_system="DCH"
    )
    national_roaming_pipeline_outbound = NationalRoaming(
        direction="OUT", source_system="DCH"
    )

    national_roaming_pipeline_inbound.run()
    national_roaming_pipeline_outbound.run()


if __name__ == "__main__":
    main()
