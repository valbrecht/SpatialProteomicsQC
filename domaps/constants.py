class _ConstantsClass(type):
    """A metaclass for classes that should only contain string constants."""

    def __setattr__(self, name, value):
        raise TypeError("Constants class cannot be modified")

    def get_values(cls):
        """Get all user-defined string values of the class."""
        return [
            value
            for key, value in cls.__dict__.items()
            if not key.startswith("__") and isinstance(value, str)
        ]


class DataFrameStrings(metaclass=_ConstantsClass):
    # Indexing levels
    EXPERIMENT = "Experiment"  # Refers to a single set of maps that can be loaded into a SpatialDataSet
    MAP = "Map"  # Refers to a single set of samples that make up one map
    FRACTION = "Fraction"  # Refers to a fraction of the experimental gradient
    SET = "Set"  # Refers to a set of column that contain the same kind of data
    EXP_MAP = "Exp_Map"  # A combination of experiment and map used only in the SpatialDataSetComparison class

    # Column names
    PROTEIN_IDS = "Protein IDs"
    GENE_NAMES = "Gene names"
    ORIGINAL_PROTEIN_IDS = "Original Protein IDs"
    COMPARTMENT = "Compartment"
    CLUSTER = "Cluster"

    # Set names
    LFQ_INTENSITY = "LFQ intensity"
    MSMS_COUNT = "MS/MS count"
    INTENSITY = "Intensity"
    ABUNDANCE = (
        "Abundance"  # This is the generalizing one, that is used within preprocessing
    )
    RATIO = "Ratio"
    RATIO_COUNT = "Ratio count"
    RATIO_VARIABILITY = "Ratio variability"
    NORMALIZED_PROFILE = "normalized profile"
    LOG_PROFILE = "log profile"


class SettingStrings(metaclass=_ConstantsClass):
    # These are various strings used within settings files to define the processing pipeline. Changes make ols settings files incompatible.

    # Filter names
    FILTER_SILAC_COUNTVAR = "SILAC_countvar"
    FILTER_MSMS_COUNT = "msms_count"
    FILTER_CONSECUTIVE = "consecutive"

    # Normalization options
    NORMALIZATION_SUM = "sum"
    NORMALIZATION_MEDIAN = "median"

    # Acquisition modes
    SILAC_ACQUISITION = "SILAC"
    LFQ_ACQUISITION = "LFQ"
    INTENSITY_ACQUISITION = "Intensity"
    CUSTOM_ACQUISIITION = "custom"

    # Preconfigured source modes
    MAXQUANT_PROTEINS_PIVOT = "MaxQuant_proteins_pivot"
    SPECTRONAUT_PROTEINS_LONG = "Spectronaut_proteins_long"

    # Acquisition mode settings used to define which sets should be read and how they should be processed
    INPUT_INVERT = "input_invert"
    INPUT_LOGGED = "input_logged"
    INPUT_SAMPLENORMALIZATION = "input_samplenormalization"
    QUALITY_FILTER = "quality_filter"
    AVERAGE_MSMS_COUNTS = "average_MSMS_counts"
    CONSECUTIVE = "consecutive"
    RATIOCOUNT = "RatioCount"
    RATIOVARIABILITY = "RatioVariability"

    # Source settings used to define how the data should be read and formatted
    ORIGINAL_PROTEIN_IDS = "original_protein_ids"
    GENES = "genes"
    COLUMN_FILTERS = "column_filters"
    ANNOTATION_COLUMNS = "columns_annotation"
    SAMPLES = "samples"
    ORIENTATION = "orientation"

    # General settings
    SETS = "sets"
    SOURCE = "source"
    ACQUISITION = "acquisition"
    COMMENT = "comment"
    NAME_PATTERN = "name_pattern"
    ORGANISM = "organism"
    REANNOTATE = "reannotate"
    REANNOTATION_SOURCE = "reannotation_source"
    ORGANELLES = "organelles"
    COMPLEXES = "complexes"
