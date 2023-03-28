import asyncio
from pathlib import Path

import rasterio
from rio_cogeo import cog_info
from rio_cogeo.cogeo import cog_translate

from ingest.config import datasets_folder, gdal_configs, logging, raw_folder
from ingest.ingest_exceptions import RasterUploadError
from ingest.utils import upload_error_blob, upload_ingesting_blob

logger = logging.getLogger(__name__)

def ingest_raster_sync(vsiaz_blob_path: str):
    # is_valid, errors, warnings = cog_validate(vsiaz_blob_path)
    config, output_profile = gdal_configs()
    # logger.info(f'using COG profile {json.dumps(dict(output_profile), indent=4)} and config {json.dumps(dict(config), indent=4)}')
    path = Path(vsiaz_blob_path)

    dname = str(path).replace(f"/{raw_folder}/", f"/{datasets_folder}/")
    fname, _ = path.name.rsplit(".", 1)
    try:
        with rasterio.open(vsiaz_blob_path, "r") as src_dataset:
            if src_dataset.colorinterp:
                out_cog_dataset_path = f"{dname}/{fname}.tif"
                logger.info(f"Creating COG {out_cog_dataset_path}")
                asyncio.run(upload_ingesting_blob(out_cog_dataset_path))
                cog_translate(
                    source=src_dataset,
                    dst_path=out_cog_dataset_path,
                    dst_kwargs=output_profile,
                    config=config,
                    web_optimized=True,
                    forward_ns_tags=True,
                    forward_band_tags=True,
                    use_cog_driver=True,
                )
                logger.info(f"COG created: {out_cog_dataset_path}.")
            else:
                for bandindex in src_dataset.indexes:
                    out_cog_dataset_path = f"{dname}/{fname}_band{bandindex}.tif"
                    logger.info(f"Converting band {bandindex} from {vsiaz_blob_path}")
                    cog_translate(
                        source=src_dataset,
                        dst_path=out_cog_dataset_path,
                        indexes=[bandindex],
                        dst_kwargs=output_profile,
                        config=config,
                        web_optimized=True,
                        forward_ns_tags=True,
                        forward_band_tags=True,
                        use_cog_driver=False,
                    )

            # logger.info(json.dumps(json.loads(cog_info(out_cog_dataset_path).json()), indent=4) )
            # exit()
    except RasterUploadError as e:
        logger.error(
            f"Error creating COG from {vsiaz_blob_path}: {e}. Uploading error blob"
        )
        asyncio.run(
            upload_error_blob(
                vsiaz_blob_path,
                f"Error creating COG from {vsiaz_blob_path}: {e}. Uploading error blob",
            )
        )



async def ingest_raster(vsiaz_blob_path: str):
    # is_valid, errors, warnings = cog_validate(vsiaz_blob_path)
    config, output_profile = gdal_configs()
    # logger.info(f'using COG profile {json.dumps(dict(output_profile), indent=4)} and config {json.dumps(dict(config), indent=4)}')
    path = Path(vsiaz_blob_path)

    dname = str(path).replace(f"/{raw_folder}/", f"/{datasets_folder}/")
    fname, _ = path.name.rsplit(".", 1)
    try:
        with rasterio.open(vsiaz_blob_path, "r") as src_dataset:
            if src_dataset.colorinterp:
                out_cog_dataset_path = f"{dname}/{fname}.tif"
                logger.info(f"Creating COG {out_cog_dataset_path}")
                await upload_ingesting_blob(out_cog_dataset_path)
                cog_translate(
                    source=src_dataset,
                    dst_path=out_cog_dataset_path,
                    dst_kwargs=output_profile,
                    config=config,
                    web_optimized=True,
                    forward_ns_tags=True,
                    forward_band_tags=True,
                    use_cog_driver=True,
                )
                logger.info(f"COG created: {out_cog_dataset_path}.")
            else:
                for bandindex in src_dataset.indexes:
                    out_cog_dataset_path = f"{dname}/{fname}_band{bandindex}.tif"
                    logger.info(f"Converting band {bandindex} from {vsiaz_blob_path}")
                    cog_translate(
                        source=src_dataset,
                        dst_path=out_cog_dataset_path,
                        indexes=[bandindex],
                        dst_kwargs=output_profile,
                        config=config,
                        web_optimized=True,
                        forward_ns_tags=True,
                        forward_band_tags=True,
                        use_cog_driver=False,
                    )

            # logger.info(json.dumps(json.loads(cog_info(out_cog_dataset_path).json()), indent=4) )
            # exit()
    except RasterUploadError as e:
        logger.error(
            f"Error creating COG from {vsiaz_blob_path}: {e}. Uploading error blob"
        )
        await upload_error_blob(
            vsiaz_blob_path,
            f"Error creating COG from {vsiaz_blob_path}: {e}. Uploading error blob",
        )
