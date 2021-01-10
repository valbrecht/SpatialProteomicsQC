class SpatialDataSet:

    def __init__(self, **kwargs):
        """Import of the raw file of interest. Dataframe will be generated, which contains only the data of desired
        column names, specified by the dictionary entry regex["col_shortened"]

        Dictionaries are created, that ate used for filtering and plotting, respectively.

        Args:
            filename: raw file obtained by the LFQ/SILAC approach (Protein Groups Files), processed by MaxQuant

        Returns:
            df_original: shortened data frame, contains only the information, which was determined due to
            the values of the key "col_shortened"
        """
        # df_original contains all information of the raw file; tab separated file is imported,
        # without considering comments, marked with #

        self.filename = "6_deep_maps.txt" if "filename" not in kwargs.keys() else kwargs["filename"]
        self.json_filename = "AnalysedDatasets.json" if "json_filename" not in kwargs.keys() else kwargs["json_filename"]
        
        
        self.map_of_interest = "MAP1" if "map_of_interest" not in kwargs.keys() else kwargs["map_of_interest"]
        self.cluster_of_interest = "Proteasome" if "cluster_of_interest" not in kwargs.keys() else kwargs[
            "cluster_of_interest"]
        
        self.cluster_of_interest_comparison = "Proteasome" if "cluster_of_interest_comparison" not in kwargs.keys() else kwargs[
            "cluster_of_interest_comparison"]

        self.summed_MSMS_counts = 2 if "summed_MSMS_counts" not in kwargs.keys() else kwargs["summed_MSMS_counts"]
        self.consecutiveLFQi = 4 if "consecutiveLFQi" not in kwargs.keys() else kwargs["consecutiveLFQi"]
        
        self.RatioHLcount_1 = 3 if "RatioHLcount_1" not in kwargs.keys() else kwargs["RatioHLcount_1"]
        self.RatioHLcount_2 = 2 if "RatioHLcount_2" not in kwargs.keys() else kwargs["RatioHLcount_2"]
        self.RatioVariability = 30 if "RatioVariability" not in kwargs.keys() else kwargs["RatioVariability"]
            
        self.collapse_maps = False if "collapse_maps" not in kwargs.keys() else kwargs["collapse_maps"]
        
        self.collapse_maps_PCA = False if "collapse_maps_PCA" not in kwargs.keys() else kwargs["collapse_maps_PCA"]
        
        self.multi_choice_venn = ["x", "y"] if "multi_choice" not in kwargs.keys() else kwargs["multi_choice"]
        self.multi_choice = ["x", "y"] if "multi_choice" not in kwargs.keys() else kwargs["multi_choice"]
        
        self.multi_choice_venn = ["x", "y"] if "multi_choice_venn" not in kwargs.keys() else kwargs["multi_choice_venn"]
        
        self.regex = {
            "imported_columns": "^[Rr]atio H/L (?!normalized|type|is.*).+|id$|[Mm][Ss].*[cC]ount.+$|[Ll][Ff][Qq].*|.*[nN]ames.*|.*[Pp][rR].*[Ii][Dd]s.*|[Pp]otential.[cC]ontaminant|[Oo]nly.[iI]dentified.[bB]y.[sS]ite|[Rr]everse|[Ss]core|[Qq]-[Vv]alue|R.Condition|PG.Genes|PG.ProteinGroups|PG.Cscore|PG.Qvalue|PG.RunEvidenceCount|PG.Quantity",
#            "index_col_silac": "[Pp]rotein.[Ii][Dd]s|[Mm]ajority.[Pp]rotein.[Ii][Dd]s|[Pp]rotein.[Nn]ames|[Gg]ene.[Nn]ames|[Ii][Dd]|[Ss]core|[Qq]-[Vv]alue",
#            "index_col_lfq": ".*[Pp][rR].*[Ii][Dd]s.*|.*[nN]ames.*|[Ii][Dd]|[Ss]core|[Qq]-[Vv]alue|MS/MS.count$",

#            "type_count_silac": "([Rr]atio.[Hh]/[Ll].[cC]ount)[ .].*_.*K",
#            "type_var_silac": "([Rr]atio.[Hh]/[Ll].[Vv]ariability....)[ .].*_.*K",
#            "type_ratio_silac": "([rR]atio.[Hh]/[Ll])[ .](?![cC]ount|[Vv]ariability).*_.*K",
#
#            "type_count_lfq": "([Rr]atio.[Hh]/[Ll].[cC]ount)[ .].*_.*K",
#            "type_var_lfq": "([Rr]atio.[Hh]/[Ll].[Vv]ariability....)[ .].*_.*K",
#            "type_ratio_silac": "([rR]atio.[Hh]/[Ll])[ .](?![cC]ount|[Vv]ariability).*_.*K",
#
#            "type_msms_lfq": "([Mm][Ss]/[Mm][Ss].[cC]ount)[ .].*_.*K",
#            "type_intensity_lfq": "([Ll][Ff][Qq].[Ii]ntensity)[ .].*_.*K",

            # "type_lfq": "(.*[nNTt]{1}[yYtT]{1})[ .].*_\d+[Kk]$",

            #"lfq_nan": "[Ll][Ff][Qq].*",

            #"contaminants": "[Pp]otential.[cC]ontaminant",
            #"sites": "[Oo]nly.[iI]dentified.[bB]y.[sS]ite",
            #"reverse": "[Rr]everse"
        }
        
        markerprotein_human = {
            "Proteasome": ["PSMA1", "PSMA2", "PSMA3", "PSMA4", "PSMA5", "PSMA6", "PSMA7", "PSMB1", "PSMB2", "PSMB3",
                           "PSMB4", "PSMB5", "PSMB6", "PSMB7"],
            "CCT complex": ["CCT2", "CCT3", "CCT4", "CCT5", "CCT6A", "CCT7", "CCT8","CCT6B", "TCP1"],
            "V-type proton ATPase": ["ATP6AP1", "ATP6V0A1", "ATP6V0A2", "ATP6V0A4", "ATP6V0D1", "ATP6V1A", "ATP6V1B2",
                                     "ATP6V1C1", "ATP6V1E1", "ATP6V1G1", "ATP6V1H"],
            "EMC": ["EMC1", "EMC2", "EMC3", "EMC4", "EMC7", "EMC8", "EMC10","EMC6","EMC9"],
            "Lysosome" : ["LAMTOR1", "LAMTOR2", "LAMTOR3", "LAMTOR4", "LAMTOR5", "LAMP1", "LAMP2", "CTSA", "CTSB", "CTSC", "CTSD", "CTSL", "CTSZ"]
            }
        
        self.all_markerproteins = {
            "Human - Swissprot" : markerprotein_human, 
            "Arabidopsis - Araport" : {
                "CCT complex": ["AT3G11830","AT5G16070","AT5G20890","AT5G26360","AT1G24510","AT3G18190","AT3G20050","AT3G03960"],
                "Coatomer": ["AT1G62020","AT4G34450","AT4G31490","AT1G79990","AT1G30630","AT4G08520"],
                "SAGA complex": ["AT5G25150","AT3G54610","AT1G54360","AT1G54140","AT4G38130","AT4G31720"],
                "AP1/2": ["AT1G60070","AT2G17380","AT4G23460","AT5G22780","AT1G47830","AT5G46630","AT1G10730"],
                "20S proteasome": ["AT1G13060","AT1G21720","AT3G22110","AT3G22630","AT5G40580","AT1G16470","AT1G47250","AT1G53850",
                                  "AT1G56450","AT2G27020","AT3G60820","AT4G31300","AT5G35590","AT3G51260","AT3G53230"],
                "cis Golgi proteins": ["AT1G05720","AT1G07230","AT1G10950","AT1G15020","AT1G18580","AT1G20270","AT1G29060","AT1G29310",
                                      "AT1G51590","AT1G52420","AT1G53710","AT1G62330","AT1G65820","AT1G76270","AT1G77370","AT1G78920",
                                      "AT2G01070","AT2G14740","AT2G17720","AT2G20130","AT2G20810","AT2G40280","AT2G43080","AT2G47320",
                                      "AT3G06300","AT3G09090","AT3G21160","AT3G24160","AT3G28480","AT3G48280","AT4G01210","AT4G24530",
                                      "AT5G04480","AT5G06660","AT5G14430","AT5G14950","AT5G18900","AT5G27330","AT5G47780","AT5G65470",
                                      "AT5G66060"],
                "photosystem": ["AT2G33040","AT5G13450","ATCG00280","AT1G31330","AT1G29920","ATCG00340","ATCG00350","AT1G61520",
                               "ATCG00580","ATCG00710","AT4G12800","AT4G10340","AT3G08940","AT3G54890","ATCG00270","ATCG00020",
                               "AT5G13440","AT1G55670","AT4G22890","AT3G47470","AT1G45474"]
            },
            "Mouse - Swissprot" : {
                "STH" : ["STH"],
            },
            }
                    
        
        self.markerproteins = markerprotein_human if "markerprotein" not in kwargs.keys() else kwargs["markerprotein"]
        
        self.acquisition = "SILAC" if "acquisition" not in kwargs.keys() else kwargs["acquisition"]
        
        #self.cache_comparison = False if "cache_comparison" not in kwargs.keys() else kwargs["cache_comparison"]
        
        self.acquisition_set_dict = {
            "LFQ": ["[Ll][Ff][Qq].[Ii]ntensity", "[Mm][Ss]/[Mm][Ss].[cC]ount", "[Ii]ntensity"],
            "LFQ Spectronaut" : ["LFQ intensity", "MS/MS count"],
            "SILAC"  : [ "[Rr]atio.[Hh]/[Ll](?!.[Vv]aria|.[Cc]ount)","[Rr]atio.[Hh]/[Ll].[Vv]ariability.\[%\]", "[Rr]atio.[Hh]/[Ll].[cC]ount"]
            }
        
        self.name_pattern = ".* (?P<cond>.*)_(?P<rep>.*)_(?P<frac>.*)" if "name_pattern" not in kwargs.keys() else kwargs["name_pattern"]
        
        self.fraction_dict = {"1K": "01K","3K": "03K", "6K": "06K", "12K": "12K", "24K": "24K", "80K": "80K", 
                              "01K": "01K","03K": "03K", "06K": "06K", "012K": "12K", "024K": "24K", "080K": "80K", 
                              "Cyt": "Cyt", "Mem": "Mem", "Nuc": "Nuc", "Prot": "Prot", "cyt": "Cyt", "mem": "Mem", "nuc": "Nuc", "Prot": "Prot", "prot": "Prot"}
        
        self.Spectronaut_columnRenaming = {
            "R.Condition": "Map", "PG.Genes" : "Gene names", "PG.Qvalue": "Q-value", "PG.Cscore":"C-Score", 
            "PG.ProteinGroups" : "Protein IDs", "PG.RunEvidenceCount" : "MS/MS count", "PG.Quantity" : "LFQ intensity"
            }
        
        self.analysed_datasets_dict = {}
        self.analysis_summary_dict = {}
        self.shape_dict = {}  
        self.expname = "Protein_Groups" if "expname" not in kwargs.keys() else kwargs["expname"]      
        
        css_color_string='''
            green, blue, orange, purple, goldenrod, yellow, lightcoral, magenta, brown, lightpink, red, turquoise,
            khaki, darkgoldenrod,darkturquoise, darkviolet, greenyellow, darksalmon, hotpink, indianred, indigo,darkolivegreen, coral, aqua, aquamarine, azure,
            beige, bisque, black, blanchedalmond, blueviolet, burlywood, cadetblue, yellowgreen, chartreuse, chocolate, cornflowerblue, cornsilk, crimson, cyan, darkblue, darkcyan,
            darkgray, darkgrey, darkgreen, darkkhaki, darkmagenta, darkorange, darkorchid, darkred, darkseagreen, darkslateblue, darkslategray, darkslategrey,
            deeppink, deepskyblue, dimgray, dimgrey, dodgerblue, firebrick, floralwhite, forestgreen, fuchsia, gainsboro, ghostwhite, gold, gray, grey, 
            ivory, lavenderblush, lawngreen, lemonchiffon, lightblue, lightcyan, lightgoldenrodyellow, lightgray, lightgrey, lightgreen, lightsalmon, lightseagreen,
            lightskyblue, lightslategray, lightslategrey, lightsteelblue, lightyellow, lime, limegreen, linen, maroon, mediumaquamarine, mediumblue, mediumorchid, mediumpurple,
            mediumseagreen, mediumslateblue, mediumspringgreen, mediumturquoise, mediumvioletred, midnightblue, mintcream, mistyrose, moccasin, navajowhite, navy, oldlace, olive, 
            olivedrab, orangered, orchid, palegoldenrod, palegreen, paleturquoise, palevioletred, papayawhip, peachpuff, peru, pink,
            plum, powderblue, rosybrown, royalblue, saddlebrown, salmon, sandybrown, seagreen, seashell, sienna, silver, skyblue, slateblue, slategray, slategrey, snow, springgreen,
            steelblue, teal, thistle, tomato, violet, wheat, white, whitesmoke, 
            '''
        css_color=css_color_string.split(',')
        css_color=[l.replace('\n','') for l in css_color]
        css_color=[l.replace(' ','') for l in css_color]
        self.css_color = css_color 
        
    def data_reading(self):
        """Data import.

        Args:
            filename: stored as attribute

        Returns:
            df_orginal: raw, unprocessed dataframe, single level column index
        """

        self.df_original = pd.read_csv(self.filename, sep="\t", comment="#",
                                       usecols=lambda x: bool(re.match(self.regex["imported_columns"], x)))

        return self.df_original
    
    def processingdf(self):
        """Analysis of the SILAC/LFQ data will be performed.

        The dataframe will be filtered, normalized and converted into a dataframe, characterized by a flat column index,
        which can be used for plotting

        Args:
            acquisition mode: "SILAC" or "LFQ", which is referring to the acquisition method

        Returns:
            A dataframe, in which "Fraction" and "Map" are stacked, containing "normalized profile" as column,
            additionally "Ratio H/L count", "Ratio H/L variability [%]" is found for SILAC data and "MS/MS count"
            "LFQ intensity" for LFQ data; represented as a flat column index
        """
    
        def indexingdf(df_original, acquisition_set_dict, acquisition, fraction_dict, name_pattern, shape_dict):
            """For data output from MaxQuant, all columns - except of "MS/MS count" and "LFQ intensity" (LFQ) | 
            "Ratio H/L count", "Ratio H/L variability [%]" (SILAC) - will be set as index.
            A multiindex will be generated, containing "Set" ("MS/MS count", "LFQ intensity"|  "Ratio H/L count", "Ratio H/L variability [%]"),
            "Fraction" (= defined via "name_pattern") and "Map" (= defined via "name_pattern") as level labels,
            allowing the stacking and unstacking of the dataframe;
            The dataframe will be filtered by removing matches to the reverse database, matches only identified by
            site, and potential contaminants.
            
            Args:
                df_original: dataframe, columns defined through self.regex["imported_columns"]
                

            Returns:
                df_index: mutliindex dataframe, which contains 3 level labels: MAP, Fraction, Type
            """
            
            # deep copy of the dataframe
            df_original = df_original.copy()
            df_i = df_original.set_index([col for col in df_original.columns if any([re.match(s, col) 
                                                                                     for s in self.acquisition_set_dict[self.acquisition]]) == False])
    
            # multindex will be generated, by isolating the information about the Map, Fraction and Type from each
            # individual column name
            # names=["Set", "Map", "Fraction"] defines the label of the multiindex
            multiindex = pd.MultiIndex.from_arrays(
                    arrays=[
                        [item for sublist in [[re.findall(s, col)[0] for s in self.acquisition_set_dict[self.acquisition] if re.match(s,col)] 
                                              for col in df_i.columns] for item in sublist],
                        [re.match(self.name_pattern, col).group("rep") for col in df_i.columns] if not "<cond>" in self.name_pattern 
                        else ["_".join(re.match(self.name_pattern, col).group("cond", "rep")) for col in df_i.columns],
                        [self.fraction_dict[re.match(self.name_pattern, col).group("frac")] for col in df_i.columns],
                    ],
                    names=["Set", "Map", "Fraction"]
                        )
            df_i.columns = multiindex
            df_i.sort_index(1, inplace=True)
            
            self.shape_dict["Original size"]=df_i.shape
            
            df_index = df_i.xs(
                    np.nan, 0, "Reverse").xs(
                    np.nan, 0, "Potential contaminant").xs(
                    np.nan, 0, "Only identified by site")
            df_index.replace(0, np.nan, inplace=True)
            self.shape_dict["Shape after categorical filtering"]=df_index.shape
    
            return df_index   


        def spectronaut_LFQ_indexingdf(df_original, Spectronaut_columnRenaming, acquisition_set_dict, acquisition, fraction_dict, name_pattern, shape_dict):
            """For data generated from the Spectronaut software, columns will be renamed, such it fits in the scheme of MaxQuant output data.
            Subsequently, all columns - except of "MS/MS count" and "LFQ intensity" will be set as index.
            A multiindex will be generated, containing "Set" ("MS/MS count" and "LFQ intensity"), "Fraction" (= output from Spectronaut: R.Fraction) and
            "Map" (= output from Spectronaut: R.condition). 
            A dataframe, in which "Fraction" and "Map" are stacked, containing "normalized profile" as column,
            additionally "Ratio H/L count", "Ratio H/L variability [%]" is found for SILAC data and "MS/MS count"
            for LFQ data; represented as a flat column index
            
            Args:
                df_original: dataframe, columns defined through self.regex["imported_columns"]
                

            Returns:
                df_index: mutliindex dataframe, which contains 3 level labels: MAP, Fraction, Type
            !!!
            !!!It is very important to define R.Fraction, R.condition already during the setup of Spectronaut!!!
            !!!
            """
            df_original = df_original.copy()
            
            df_renamed = df_original.rename(columns = self.Spectronaut_columnRenaming)
            
            df_renamed["Fraction"] = [re.match(name_pattern, i).group("frac") for i in df_renamed["Map"]]
            df_renamed["Map"] = [re.match(name_pattern, i).group("rep") for i in df_renamed["Map"]] if not "<cond>" in name_pattern else ["_".join(re.match(name_pattern, i).group("cond", "rep")) for i in df_renamed["Map"]]
            
            df_index = df_renamed.set_index([col for col in df_renamed.columns if any([re.match(s, col) for s in self.acquisition_set_dict[self.acquisition]]) == False])
            
            df_index.columns.names = ["Set"]
            
#df_iclass = i_class.df_index.stack(["Map", "Fraction"])
#df_iclass.columns.names = ["Set"]
#df_iclass = df_iclass.unstack(["Map", "Fraction"])
#df_iclass
            df_index = df_index.unstack(["Map", "Fraction"])
            df_index.replace(0, np.nan, inplace=True)
            df_index.rename(columns=self.fraction_dict, inplace=True)
            self.shape_dict["Original size"]=df_index.shape
            
            return df_index
        
        def stringency_silac(df_index):
            """The multiindex dataframe is subjected to stringency filtering. Only Proteins with complete profiles are
            considered (a set of f.e. 5 SILAC ratios in case you have 5 fractions / any proteins with missing values
            were rejected). Proteins were retained with 3 or more quantifications in each subfraction (=count). Furthermore,
            proteins with only 2 quantification events in one or more subfraction were retained, if their ratio
            variability for ratios obtained with 2 quantification events was below 30% (=var).
            SILAC ratios were linearly normalized by division through the fraction median. Subsequently normalization
            to SILAC loading was performed.

            Args:
                df_index: multiindex dataframe, which contains 3 level labels: MAP, Fraction, Type

            Returns:
                df_stringency_mapfracstacked: dataframe, in which "MAP" and "Fraction" are stacked;
                the columns "Ratio H/L count", "Ratio H/L variability [%]", and "Ratio H/L" stored as single level indices
            """

            # Fraction and Map will be stacked
            df_stack = df_index.stack(["Fraction", 'Map'])

            len_fractions = len(df_stack.index.get_level_values("Fraction").unique())

            # filtering for sufficient number of quantifications (count in 'Ratio H/L count'), taken
            # variability (var in Ratio H/L variability [%]) into account
            # zip: allows direct comparison of count and var
            # only if the filtering parameters are fulfilled the data will be introduced into df_countvarfiltered_stacked
            
            df_countvarfiltered_stacked = df_stack.loc[[count >= self.RatioHLcount_1 or (count >= self.RatioHLcount_2 and var < self.RatioVariability) 
                                            for var, count in zip(df_stack["Ratio H/L variability [%]"], df_stack['Ratio H/L count'])]]
            
            self.df_countvarfiltered_stacked = df_countvarfiltered_stacked
            
            self.shape_dict["Shape after Ratio H/L count (>= 3)/var (count>=2, var<30) filtering"]=df_countvarfiltered_stacked.shape

            # "Ratio H/L":normalization to SILAC loading, each individual experiment (FractionXMap) will be divided by its median
            # np.median([...]): only entries, that are not NANs are considered
            df_normsilac_stacked = df_countvarfiltered_stacked["Ratio H/L"].unstack(["Fraction", "Map"]).apply(
                lambda x: x / np.median([el for el in x if not np.isnan(el)]), axis=0).stack(["Map", "Fraction"])

            df_stringency_mapfracstacked = df_countvarfiltered_stacked[["Ratio H/L count",
                                                                    "Ratio H/L variability [%]"]].join(
                pd.DataFrame(df_normsilac_stacked, columns=["Ratio H/L"]))

            # dataframe is grouped (Map, id), that allows the filtering for complete profiles
            df_stringency_mapfracstacked = df_stringency_mapfracstacked.groupby(["Map", "id"]).filter(
                lambda x: len(x) >= len_fractions)
            
            self.shape_dict["Shape after filtering for complete profiles"]=df_stringency_mapfracstacked.shape
            
            # Ratio H/L is converted into Ratio L/H
            df_stringency_mapfracstacked["Ratio H/L"] = df_stringency_mapfracstacked["Ratio H/L"].transform(lambda x: 1 / x)
            
            
            #Annotation with marker genes
            df_eLifeMarkers = self.df_eLifeMarkers
            
            df_stringency_mapfracstacked.reset_index(inplace=True)
            df_stringency_mapfracstacked = df_stringency_mapfracstacked.merge(df_eLifeMarkers, 
                                                                              how="outer", on='Gene names', indicator = True)
            df_stringency_mapfracstacked = df_stringency_mapfracstacked.loc[df_stringency_mapfracstacked['_merge'].isin(['both',                                                                                                  'left_only'])].drop("_merge", axis=1)
            df_stringency_mapfracstacked.set_index([c for c in df_stringency_mapfracstacked.columns
                                                    if c != 'Ratio H/L count' and c != 'Ratio H/L variability [%]' and c != 'Ratio H/L'], inplace=True)
            df_stringency_mapfracstacked.rename(index={np.nan : "undefined"}, level='Compartment', inplace=True)


            return df_stringency_mapfracstacked


        def normalization_01_silac(df_stringency_mapfracstacked):
            """The multiindex dataframe, that was subjected to stringency filtering, is 0-1 normalized ("Ratio H/L").

            Args:
                df_stringency_mapfracstacked: dataframe, in which "MAP" and "Fraction" are stacked;
                the columns "Ratio H/L count", "Ratio H/L variability [%]", and "Ratio H/L" stored as single level indices

            Returns:
                df_01_stacked: dataframe, in which "MAP" and "Fraction" are stacked; data in the column
                "Ratio H/L" is 0-1 normalized and renamed to "normalized profile"; the columns "Ratio H/L count",
                "Ratio H/L variability [%]", and "normalized profile" stored as single level indices;
                plotting is possible now
            """

            df_01norm_unstacked = df_stringency_mapfracstacked["Ratio H/L"].unstack("Fraction")

            # 0:1 normalization of Ratio L/H
            df_01norm_unstacked = df_01norm_unstacked.div(df_01norm_unstacked.sum(axis=1), axis=0)

            df_01_stacked = df_stringency_mapfracstacked[["Ratio H/L count", "Ratio H/L variability [%]"]].join(pd.DataFrame
                (df_01norm_unstacked.stack("Fraction"),columns=["Ratio H/L"]))
            #df_index[[col for col in df_index.columns if re.match(regex["lfq_nan"], col)]] = \
#df_index[[col for col in df_index.columns if re.match(regex["lfq_nan"], col)]].replace(0, np.nan)

            # "Ratio H/L" will be renamed to "normalized profile"
            df_01_stacked.columns = [col if col != "Ratio H/L" else "normalized profile" for col in
                                     df_01_stacked.columns]

            return df_01_stacked


        def logarithmization_silac(df_stringency_mapfracstacked):
            """The multiindex dataframe, that was subjected to stringency filtering, is logarithmized ("Ratio H/L").

            Args:
                df_stringency_mapfracstacked: dataframe, in which "MAP" and "Fraction" are stacked;
                the columns "Ratio H/L count", "Ratio H/L variability [%]", and "Ratio H/L" stored as single level indices

            Returns:
                df_log_stacked: dataframe, in which "MAP" and "Fraction" are stacked; data in the column
                "log profile" originates from logarithmized "Ratio H/L" data; the columns "Ratio H/L count",
                "Ratio H/L variability [%]" and  "log profile" are stored as single level indices; PCA is possible now

            """
            # logarithmizing, basis of 2
            df_lognorm_ratio_stacked = df_stringency_mapfracstacked["Ratio H/L"].transform(np.log2)
            df_log_stacked = df_stringency_mapfracstacked[["Ratio H/L count", "Ratio H/L variability [%]"]].join(
                pd.DataFrame(df_lognorm_ratio_stacked, columns=["Ratio H/L"]))

            # "Ratio H/L" will be renamed to "log profile"
            df_log_stacked.columns = [col if col != "Ratio H/L" else "log profile" for col in df_log_stacked.columns]

            return df_log_stacked

        
        def stringency_lfq(df_index):
            """The multiindex dataframe is subjected to stringency filtering. Only Proteins which were identified with
            at least [4] consecutive data points regarding the "LFQ intensity", and if summed MS/MS counts >= n(fractions)*[2]
            (LFQ5: min 10 and LFQ6: min 12, respectively; coverage filtering) were included.

            Args:
                df_index: multiindex dataframe, which contains 3 level labels: MAP, Fraction, Typ

            Returns:
                df_stringency_mapfracstacked: dataframe, in which "Map" and "Fraction" is stacked;
                "LFQ intensity" and "MS/MS count" define a single-level column index
                """

            # retrieve number of fractions that are present in the dataset
            df_fractionnumber_stacked = df_index.copy().stack("Fraction")
            number_fractions = len(df_fractionnumber_stacked.index.get_level_values("Fraction").unique())

            df_index = df_index.stack("Map")

            # sorting the level 0, in order to have LFQ intensity -	MS/MS count instead of continuous alternation
            df_index.sort_index(axis=1, level=0, inplace=True)

            # "MS/MS count"-column: take the sum over the fractions;
            # if the sum is larger than n[fraction]*2, it will be stored in the new dataframe
            df_mscount_mapstacked = df_index.loc[df_index[('MS/MS count')].apply(np.sum, axis=1) >= (
                    number_fractions * self.summed_MSMS_counts)]

            self.shape_dict["Shape after MS/MS value filtering"]=df_mscount_mapstacked.shape
            
            df_stringency_mapfracstacked = df_mscount_mapstacked.copy()

            # series no dataframe is generated; if there are at least i.e. 4 consecutive non-NANs, data will be retained
            df_stringency_mapfracstacked = df_stringency_mapfracstacked.loc[
                df_stringency_mapfracstacked[("LFQ intensity")].apply(lambda x: any(
                    np.invert(np.isnan(x)).rolling(window=self.consecutiveLFQi).sum() >=
                    self.consecutiveLFQi), axis=1)]
            
            self.shape_dict["Shape after consecutive value filtering"]=df_stringency_mapfracstacked.shape

            df_stringency_mapfracstacked = df_stringency_mapfracstacked.copy().stack("Fraction")
            
            #Annotation with marker genes
            df_eLifeMarkers = self.df_eLifeMarkers
            
            df_stringency_mapfracstacked.reset_index(inplace=True)
            df_stringency_mapfracstacked = df_stringency_mapfracstacked.merge(df_eLifeMarkers, 
                                                                              how="outer", on='Gene names', indicator = True)
            df_stringency_mapfracstacked = df_stringency_mapfracstacked.loc[df_stringency_mapfracstacked['_merge'].isin(['both',                                                                                                  'left_only'])].drop("_merge", axis=1)
            df_stringency_mapfracstacked.set_index([c for c in df_stringency_mapfracstacked.columns
                                                    if c != 'MS/MS count' and c != 'LFQ intensity'], inplace=True)
            df_stringency_mapfracstacked.rename(index={np.nan : "undefined"}, level='Compartment', inplace=True)
            
            return df_stringency_mapfracstacked


        def normalization_01_lfq(df_stringency_mapfracstacked):
            """The multiindex dataframe, that was subjected to stringency filtering, is 0-1 normalized ("LFQ intensity").

            Args:
                df_stringency_mapfracstacked: dataframe, in which "Map" and "Fraction" is stacked;
                "LFQ intensity" and "MS/MS count" define a single-level column index


            Returns:
                df_01_stacked: dataframe, in which "MAP" and "Fraction" are stacked; data in the column
                "LFQ intensity" is 0-1 normalized and renamed to "normalized profile";
                the columns ""normalized profile"" and "MS/MS count" are stored as
                single level indices; plotting is possible now

            """

            df_01norm_mapstacked = df_stringency_mapfracstacked["LFQ intensity"].unstack("Fraction")

            # 0:1 normalization of Ratio L/H
            df_01norm_unstacked = df_01norm_mapstacked.div(df_01norm_mapstacked.sum(axis=1), axis=0)

            df_01_stacked = df_stringency_mapfracstacked[["MS/MS count"]].join(pd.DataFrame(df_01norm_unstacked.stack(
                   "Fraction"),columns=["LFQ intensity"]))

            # rename columns: "LFQ intensity" into "normalized profile"
            df_01_stacked.columns = [col if col != "LFQ intensity" else "normalized profile" for col in
                                     df_01_stacked.columns]
            
            #retrieve number of non valid profiles - profiles that contain NaN
            series_non_validProfiles = df_01_stacked.unstack(["Fraction", "Map"])["normalized profile"].apply(lambda x: x.isnull().any(), axis=1)
            non_validProfiles = len(series_non_validProfiles[series_non_validProfiles == True].index)
            self.shape_dict["Non valid profiles"] = non_validProfiles
            
            #imputation
            df_01_stacked = df_01_stacked.unstack("Fraction").replace(np.NaN, 0).stack("Fraction")
            
            df_01_stacked = df_01_stacked.sort_index()
            return df_01_stacked


        def logarithmization_lfq(df_stringency_mapfracstacked):
            """The multiindex dataframe, that was subjected to stringency filtering, is logarithmized ("LFQ intensity").

            Args:
                df_stringency_mapfracstacked: dataframe, in which "Map" and "Fraction" is stacked;
                "LFQ intensity" and "MS/MS count" define a single-level column index

            Returns:
                df_log_stacked: dataframe, in which "MAP" and "Fraction" are stacked; data in the column "log profile"
                originates from logarithmized  "LFQ intensity"; the columns "log profile" and "MS/MS count" are
                stored as single level indices; PCA is possible now
            """

            df_lognorm_ratio_stacked = df_stringency_mapfracstacked["LFQ intensity"].transform(np.log2)
            #df_log_stacked = df_stringency_mapfracstacked.copy()
            #df_log_stacked["LFQ intensity"] = df_lognorm_mapstacked
            #df_log_stacked = df_log_stacked.fillna(0).stack("Fraction")

            df_log_stacked = df_stringency_mapfracstacked[["MS/MS count"]].join(pd.DataFrame
                (df_lognorm_ratio_stacked, columns=["LFQ intensity"]))

            # "Ratio H/L" will be renamed to "log profile"
            df_log_stacked.columns = [col if col != "LFQ intensity" else "log profile" for col in df_log_stacked.columns]

            return df_log_stacked


        if self.acquisition == "SILAC":
            df_index = indexingdf(self.df_original, self.acquisition_set_dict, self.acquisition, self.fraction_dict, self.name_pattern, self.shape_dict)
            self.df_index = df_index
            df_stringency_mapfracstacked = stringency_silac(df_index)
            df_01_stacked = normalization_01_silac(df_stringency_mapfracstacked)
            df_log_stacked = logarithmization_silac(df_stringency_mapfracstacked)
            self.df_log_stacked = df_log_stacked
            self.df_01_stacked = df_01_stacked
            fractions = df_01_stacked.index.get_level_values("Fraction").unique()
            self.fractions = fractions
            map_names = self.df_01_stacked.index.get_level_values("Map").unique()
            self.map_names = map_names
            
            unique_proteins = list(dict.fromkeys([i.split(";")[0] for i in df_01_stacked.reset_index()["Protein IDs"]]))
            #number_unique_proteins = len(unique_proteins)
            self.analysis_summary_dict["Unique Proteins"] = unique_proteins
            
            self.analysis_summary_dict["changes in Shape after filtering"] = self.shape_dict.copy() 
            self.analysis_parameters = {"acquisition" : self.acquisition, 
                                        "filename" : self.filename,
                                        "Ratio H/L count 1 (>= X)" : self.RatioHLcount_1,
                                        "Ratio H/L count 2 (>=Y, var<Z)" : self.RatioHLcount_2,
                                        "Ratio variability (<Z, count>=Y)" : self.RatioVariability}
            
            self.analysis_summary_dict["Analysis parameters"] = self.analysis_parameters.copy() 
            self.analysed_datasets_dict[self.expname] = self.analysis_summary_dict.copy() 

            self.shape_dict.clear()
            self.analysis_parameters.clear() 
            return self.df_01_stacked


        #elif self.acquisition == "LFQ":
        elif self.acquisition == "LFQ" or self.acquisition == "LFQ Spectronaut":
            if self.acquisition == "LFQ":
                df_index = indexingdf(self.df_original, self.acquisition_set_dict, self.acquisition, self.fraction_dict, self.name_pattern, self.shape_dict)
            elif self.acquisition == "LFQ Spectronaut":
                df_index = spectronaut_LFQ_indexingdf(self.df_original, self.Spectronaut_columnRenaming, self.acquisition_set_dict, self.acquisition, self.fraction_dict, self.name_pattern, self.shape_dict)
            
            self.df_index = df_index           
            df_stringency_mapfracstacked = stringency_lfq(df_index)
            df_01_stacked = normalization_01_lfq(df_stringency_mapfracstacked)
            df_log_stacked = logarithmization_lfq(df_stringency_mapfracstacked)
            self.df_log_stacked = df_log_stacked
            self.df_01_stacked = df_01_stacked
            fractions = df_01_stacked.index.get_level_values("Fraction").unique()
            self.fractions = fractions
            map_names = self.df_01_stacked.index.get_level_values("Map").unique()
            self.map_names = map_names
            
            unique_proteins = list(dict.fromkeys([i.split(";")[0] for i in df_01_stacked.reset_index()["Protein IDs"]]))
            #number_unique_proteins = len(unique_proteins)
            self.analysis_summary_dict["Unique Proteins"] = unique_proteins
            
            self.analysis_summary_dict["changes in Shape after filtering"] = self.shape_dict.copy() 
            self.analysis_parameters = {"acquisition" : self.acquisition, 
                            "filename" : self.filename,
                            "consecutive data points" : self.consecutiveLFQi,
                            "summed MS/MS counts" : self.summed_MSMS_counts}
            self.analysis_summary_dict["Analysis parameters"] = self.analysis_parameters.copy() 
            self.analysed_datasets_dict[self.expname] = self.analysis_summary_dict.copy() 
            
            self.shape_dict.clear()
            self.analysis_parameters.clear() 
            return self.df_01_stacked

        else:
            return "I don't know this"    
        
#list_drop_col = [column for column in df_index.columns if not column.startswith("Ratio ")]
#list_endcount = [column for column in df_index.columns if column.endswith("count")]
#list_endpct = [column for column in df_index.columns if column.endswith("[%]")]
#list_drop_col.extend(list_endcount)
#list_drop_col.extend(list_endpct)
#df_index = df_index.drop(list_drop_col, axis=1)
#df_index[[col for col in df_index.columns if re.match(regex["lfq_nan"], col)]] = \
#df_index[[col for col in df_index.columns if re.match(regex["lfq_nan"], col)]].replace(0, np.nan)
            
    def perform_pca(self):
        """PCA will be performed, using logarithmized data.

        Args:
            self.df_log_stacked: dataframe, in which "MAP" and "Fraction" are stacked; data in the column "log profile"
                originates from logarithmized  "LFQ intensity" and "Ratio H/L", respectively; additionally the columns
                "MS/MS count" and "Ratio H/L count|Ratio H/L variability [%]" are stored as single level indices

        Returns:
                df_pca_all_marker_cluster_maps: PCA processed dataframe, containing the columns "PC1", "PC2", "PC3",
                filtered for marker genes, that are consistent throughout all maps / coverage filtering.
        """

        markerproteins = self.markerproteins

        if self.acquisition == "SILAC":
            df_01orlog_fracunstacked = self.df_log_stacked["log profile"].unstack("Fraction").dropna()
        elif self.acquisition == "LFQ" or self.acquisition == "LFQ Spectronaut":
            df_01orlog_fracunstacked = self.df_01_stacked["normalized profile"].unstack("Fraction").dropna()
        
            
        pca = PCA(n_components=3)

        # df_pca: PCA processed dataframe, containing the columns "PC1", "PC2", "PC3"
        df_pca = pd.DataFrame(pca.fit_transform(df_01orlog_fracunstacked))
        df_pca.columns = ["PC1", "PC2", "PC3"]
        df_pca.index = df_01orlog_fracunstacked.index
        self.df_pca = df_pca
        
        map_names = self.map_names
        df_pca_all_marker_cluster_maps_unfiltered = pd.DataFrame()
        for maps in map_names:
            for clusters in markerproteins:
                for marker in markerproteins[clusters]:
                    if marker not in df_pca.index.get_level_values("Gene names"):
                        continue
                    plot_try_pca = df_pca.xs((marker, maps), level=["Gene names", "Map"], drop_level=False)
                    df_pca_all_marker_cluster_maps_unfiltered = df_pca_all_marker_cluster_maps_unfiltered.append(
                        plot_try_pca)
    
        # genes are droped, if they are not present in all maps
        df_pca_all_marker_cluster_maps = df_pca_all_marker_cluster_maps_unfiltered.groupby(["Gene names"]).filter(
            lambda x: len(x) >= len(map_names))
        self.df_pca_all_marker_cluster_maps = df_pca_all_marker_cluster_maps

        
    def plot_global_pca(self):
        """"
        PCA plot will be generated

        Args:
            df_pca: PCA processed dataframe, containing the columns "PC1", "PC2", "PC3",
                    index: "Gene names" 	"Protein IDs" 	"C-Score" 	"Q-value" 	"Map" 	"Compartment" 	

        Returns:
            pca_figure: global PCA plot
        """
        
        compartments = self.df_eLifeMarkers["Compartment"].unique()
        compartment_color = dict(zip(compartments, self.css_color))
        compartment_color["undefined"] = "lightgrey"
        
        if self.collapse_maps_PCA == False:
            df_global_pca = self.df_pca.unstack("Map").swaplevel(0,1, axis=1)[self.map_of_interest].reset_index()
        else:
            df_global_pca = self.df_pca.rename_axis("PC", axis="columns").unstack("Map").stack("PC").median(axis=1).to_frame().unstack("PC")
            df_global_pca.columns = df_global_pca.columns.droplevel()
            df_global_pca.reset_index(inplace=True)

        
        fig_global_pca = px.scatter(data_frame=df_global_pca,
                                    x="PC1",
                                    y="PC3",
                                    color="Compartment",
                                    color_discrete_map=compartment_color,
                                    title="Protein subcellular localization by PCA",
                                    hover_data=["Gene names", "Compartment"], #"Protein names", 
                            #       custom_data=df_annotated_all.columns,
                                    opacity=0.9
                                    )
        return fig_global_pca                         
            
            
    def plot_pca(self):
        """
        PCA plot will be generated

        Args:
            df_pca_all_marker_cluster_maps: PCA processed dataframe, containing the columns "PC1", "PC2", "PC3",
                filtered for marker genes, that are consistent throughout all maps / coverage filtering.

        Returns:
            pca_figure: PCA plot, for one protein cluster all maps are plotted
        """

        df_pca_all_marker_cluster_maps = self.df_pca_all_marker_cluster_maps
        map_names = self.map_names
        markerproteins = self.markerproteins

        for maps in map_names:
            df_setofproteins_PCA = pd.DataFrame()
            for marker in markerproteins[self.cluster_of_interest]:
                if marker not in df_pca_all_marker_cluster_maps.index.get_level_values("Gene names"):
                    continue
                plot_try_pca = df_pca_all_marker_cluster_maps.xs((marker, maps), level=["Gene names", "Map"],
                                                                 drop_level=False)
                df_setofproteins_PCA = df_setofproteins_PCA.append(plot_try_pca)

            df_setofproteins_PCA.reset_index(inplace=True)
            if maps == map_names[0]:
                pca_figure = go.Figure(
                    data=[go.Scatter3d(x=df_setofproteins_PCA.PC1, y=df_setofproteins_PCA.PC2, z=df_setofproteins_PCA.PC3,
                                       hovertext=df_setofproteins_PCA["Gene names"], mode="markers", name=maps
                                       # marker=dict(color=[f'rgb({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)})' for _   in range(25)])
                                       )])
            else:
                pca_figure.add_trace(go.Scatter3d(x=df_setofproteins_PCA.PC1, y=df_setofproteins_PCA.PC2, z=df_setofproteins_PCA.PC3,
                                               hovertext=df_setofproteins_PCA["Gene names"], mode="markers", name=maps
                                               ))

        pca_figure.update_layout(autosize=False, width=500, height=500,
                              title="PCA plot for <br>the protein cluster: {}".format(self.cluster_of_interest))

        return pca_figure
            

    #def plot_pca(self):
    #    """
    #    PCA plot will be generated
#
    #    Args:
    #        df_pca_for_plotting: PCA processed dataframe, containing the columns "PC1", "PC2", "PC3",
    #            filtered for marker genes, that are consistent throughout all maps / coverage filtering.
#
    #    Returns:
    #        pca_figure: PCA plot, for one protein cluster all maps are plotted
    #    """
#
    #    df_pca_for_plotting = self.df_pca_for_plotting
    #    map_names = self.map_names
    #    markerproteins = self.markerproteins
#
    #    for maps in map_names:
    #        df_setofproteins_PCA = pd.DataFrame()
    #        for marker in markerproteins[self.cluster_of_interest]:
    #            if marker not in df_pca_for_plotting.index.get_level_values("Gene names"):
    #                continue
    #            plot_try_pca = df_pca_for_plotting.xs((marker, maps), level=["Gene names", "Map"],
    #                                                             drop_level=False)
    #            df_setofproteins_PCA = df_setofproteins_PCA.append(plot_try_pca)
#
    #        df_setofproteins_PCA.reset_index(inplace=True)
    #        if maps == map_names[0]:
    #            pca_figure = go.Figure(
    #                data=[go.Scatter3d(x=df_setofproteins_PCA.PC1, y=df_setofproteins_PCA.PC2, z=df_setofproteins_PCA.PC3,
    #                                   hovertext=df_setofproteins_PCA["Gene names"], mode="markers", name=maps
    #                                   # marker=dict(color=[f'rgb({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)})' for _   in range(25)])
    #                                   )])
    #        else:
    #            pca_figure.add_trace(go.Scatter3d(x=df_setofproteins_PCA.PC1, y=df_setofproteins_PCA.PC2, z=df_setofproteins_PCA.PC3,
    #                                           hovertext=df_setofproteins_PCA["Gene names"], mode="markers", name=maps
    #                                           ))
#
    #    pca_figure.update_layout(autosize=False, width=500, height=500,
    #                          title="PCA plot for <br>the protein cluster: {}".format(self.cluster_of_interest))
#
    #    return pca_figure
#

    def plottingdf(self):
        """
        The function allows the plotting of filtered and normalized spatial proteomic data using plotly.express.
        The median profile is also calculated and displayed

        Args:
            df_ setofproteins: multiindex dataframe, that contains data about the desired protein cluster,
            stored in the columns "Ratio H/L count", "Ratio H/L variability [%]" and "normalized profile"

        Returns:
            abundance_profiles_and_median_figure: Line plot, displaying the relative abundance profiles.

        """

        df_setofproteins = self.cluster_isolation_df(self.map_of_interest, self.cluster_of_interest)

        df_setofproteins = df_setofproteins.copy()

        # fractions get sorted
        df_setofproteins = df_setofproteins.reindex(index=natsort.natsorted(df_setofproteins.index))

        df_proteinset_median = df_setofproteins["normalized profile"].unstack("Fraction").median()

        # make it available for plotting
        df_setofproteins.reset_index(inplace=True)
        abundance_profiles_figure = px.line(df_setofproteins, x="Fraction", y="normalized profile",
                                         color="Gene names",
                                         title="Relative abundance profile for {} of <br>the protein cluster: {}".format(
                                             self.map_of_interest, self.cluster_of_interest))

        df_proteinset_median.name = "normalized profile"

        #fractions get sorted
        df_proteinset_median = df_proteinset_median.reindex(index=natsort.natsorted(df_proteinset_median.index))

        # make it available for plotting
        df_proteinset_median = df_proteinset_median.reset_index()
        df_proteinset_median.insert(0, "Gene names", np.repeat("Median profile", len(df_proteinset_median)))

        abundance_profiles_and_median_figure = abundance_profiles_figure.add_scatter(x=df_proteinset_median["Fraction"],
                                                                               y=df_proteinset_median[
                                                                                   "normalized profile"],
                                                                               name="Median profile")

        return abundance_profiles_and_median_figure


    def multiple_iterations(self):
        """
        For each individual protein cluster and for each indiviual fraction the distance to the median will be calculated
        and stored in a multiindex dataframe.

        Args:
            self:
             requires dataframe (df_01_stacked, single level column), stored as attribute (self.df_01_stacked),
             in which "MAP" and "Fraction" are stacked. Additionally the columns "MS/MS count" and
             "Ratio H/L count | Ratio H/L variability [%] | Ratio H/L" are found in LFQ and SILAC data respectively.
             markerproteins, stored as attribute (self.markerproteins), that will be used for plotting

        Returns:
            df_allclusters_onlynorm_fracunstacked: multiindex dataframe, that contains only the normalized data of individual
            protein clusters substracted by the median of the respective protein cluster for each fraction. The fractions are
            unstacked.
        """

        markerproteins = self.markerproteins
        df_01_stacked = self.df_01_stacked

        df_allclusters_onlynorm_fracunstacked_unfiltered = pd.DataFrame()
        df_allclusters_01 = pd.DataFrame()

        map_names = self.map_names

        # for each individual map, and each individual protein cluster, defined in the dictionary markerproteins,
        # the functions "cluster_isolation_df" and "distance_to_median_calculation" will be performed
        for maps in map_names:
            for clusters in markerproteins:
                df_setofproteins = self.cluster_isolation_df(maps, clusters)
                df_allclusters_01 = df_allclusters_01.append(df_setofproteins)
                df_distance_to_median_fracunstacked = self.distance_to_median_calculation(df_setofproteins)
                # new column is introduced: Column name = "Cluster"; values: clustername, to wich the individual protein belongs to
                df_distance_to_median_fracunstacked["Cluster"] = clusters
                df_distance_to_median_fracunstacked.set_index("Cluster", inplace=True, append=True)
                # the isolated and processed
                df_allclusters_onlynorm_fracunstacked_unfiltered = df_allclusters_onlynorm_fracunstacked_unfiltered.append(
                    df_distance_to_median_fracunstacked)

        #storage of 0/1 normalized data in global dictionary
        ####Possibility to sort - if necessary, takes some computing time
        ####df_allclusters_01 = df_allclusters_01.reindex(index=natsort.natsorted(i_class.df_allclusters_01.index))

        self.analysis_summary_dict["0/1 normalized data"] = df_allclusters_01.reset_index().to_json() 
        # genes are droped, if they are not present in all maps
        df_allclusters_onlynorm_fracunstacked = df_allclusters_onlynorm_fracunstacked_unfiltered.groupby(["Gene names"]).filter(lambda x: len(x) >= len(map_names))
        self.df_allclusters_onlynorm_fracunstacked = df_allclusters_onlynorm_fracunstacked
        
        # concatenate both original and filtered dataframe, and drop duplicates
        dfs_dictionary = {'DF1': df_allclusters_onlynorm_fracunstacked_unfiltered,
                          'DF2': df_allclusters_onlynorm_fracunstacked}
        df = pd.concat(dfs_dictionary)
        df_genenames_sortedout = df.drop_duplicates(keep=False)
        # retrieve all gene names, that are sorted out
        genenames_sortedout_index = df_genenames_sortedout.index.get_level_values("Gene names").unique()
        genenames_sortedout_list = genenames_sortedout_index.tolist()

        self.genenames_sortedout_list = genenames_sortedout_list

        return df_allclusters_onlynorm_fracunstacked


    def cluster_isolation_df(self, maps, clusters):
        """
        The function returns a dataframe for a specified proteincluster and map, that will be hand over to the
        definition "distance_to_median_calculation"

        Args:
            maps: specified map (e.g. "MAP1")
            clusters: protein cluster, specified in self.markerproteins (e.g. "Proteasome")
            self:
                requires dataframe (df_01_stacked, single level column), stored as attribute (self.df_01_stacked),
            in which "MAP" and "Fraction" are stacked; the data in the column "normalized profile" is used for plotting.
            Additionally the columns "MS/MS count" and "Ratio H/L count | Ratio H/L variability [%] | Ratio H/L" are
            found in LFQ and SILAC data respectively
                markerproteins, stored as attribute (self.markerproteins), that will be used for plotting

        Returns:
            df_setofproteins: multiindex dataframe, that contains data about the desired protein cluster,
            stored in the columns "Ratio H/L count", "Ratio H/L variability [%]" and "normalized profile"
        """

        df_setofproteins = pd.DataFrame()
        df_01_stacked = self.df_01_stacked
        markerproteins = self.markerproteins

        # datapoints of each individual markerprotein is written into plot_try and appended to df_setofproteins
        for marker in markerproteins[clusters]:
            if marker not in df_01_stacked.index.get_level_values("Gene names"):
                continue
            plot_try = df_01_stacked.xs((marker, maps), level=["Gene names", "Map"], drop_level=False)
            df_setofproteins = df_setofproteins.append(plot_try)

        return df_setofproteins


    def distance_to_median_calculation(self, df_setofproteins):
        """
        A dataframe will be generated, in which the distances to the median profile will be stored.

        Args:
            df_setofproteins: multiindex dataframe, that contains data about the desired protein cluster,
            stored in the columns "Ratio H/L count", "Ratio H/L variability [%]" and "normalized profile"

        Returns:
            df_distance_to_median_fracunstacked: multiindex dataframe, for each individual protein and fraction the distances
            are calculated. The data is stored in single level columns (Column names: e.g. "03K", "06K", "12K", "24K", "80K")
        """
        # calculate the median of the "normalized profile" of individual proteins over the fractions
        df_proteinset_median = df_setofproteins["normalized profile"].unstack("Fraction").median()

        # substract the median individually from each entry (e.g. 03K_protein_xy - 03K_median)
        df_distance_to_median_fracunstacked = df_setofproteins["normalized profile"].unstack("Fraction")
        df_distance_to_median_fracunstacked = df_distance_to_median_fracunstacked.apply(
            lambda x: x - df_proteinset_median, axis=1)

        return df_distance_to_median_fracunstacked


    def distance_to_median_boxplot(self):
        """
        A box plot for 1 desired cluster, across all maps and fractions is generated displaying the
        distribution of the distance to the median. For each fraction, one box plot will be displayed.

        Args:
            self:
            df_allclusters_onlynorm_fracunstacked, dataframe with single level column, stored as attribute
            (self.df_allclusters_onlynorm_fracunstacked), in which "Fraction" is unstacked. It contains only the
            normalized data of individual protein clusters substracted by the median of the respective protein cluster
            for each fraction.
            map_names: individual map names are stored as an index

        Returns:
            distance_to_median_boxplot_figure: Box plot. Along the x-axis, the maps are shown, along the y-axis
            the distances is plotted
        """

        map_names = self.map_names
        df_allclusters_onlynorm_fracunstacked = self.df_allclusters_onlynorm_fracunstacked

        
        #storage of "Distances to the median profile" in global dictionary
        df_dist_to_median = abs(df_allclusters_onlynorm_fracunstacked.stack("Fraction"))
        df_dist_to_median.name = "distance"
        df_dist_to_median = df_dist_to_median.reindex(index=natsort.natsorted(df_dist_to_median.index))
        self.analysis_summary_dict["Distances to the median profile"] = df_dist_to_median.reset_index().to_json() 

        
        df_boxplot_manymaps = pd.DataFrame()

        # for each individual map and a defined cluster data will be extracted from the dataframe
        # "df_allclusters_onlynorm_fracunstacked" and appended to the new dataframe df_boxplot_manymaps
        for maps in map_names:
            plot_try = df_allclusters_onlynorm_fracunstacked.xs((self.cluster_of_interest, maps),
                                                                level=["Cluster", "Map"], drop_level=False)
            df_boxplot_manymaps = df_boxplot_manymaps.append(plot_try)

        # index will be reset, required by px.violin
        df_boxplot_manymaps = abs(df_boxplot_manymaps.stack("Fraction"))

        df_boxplot_manymaps.name = "distance"

        df_boxplot_manymaps = df_boxplot_manymaps.reindex(index=natsort.natsorted(df_boxplot_manymaps.index))

        df_boxplot_manymaps = df_boxplot_manymaps.reset_index()
                
        # box plot will be generated, every fraction will be displayed in a single plot
        distance_to_median_boxplot_figure = px.box(df_boxplot_manymaps, x="Map", y="distance", facet_col="Cluster",
                                             facet_row="Fraction",
                                             boxmode="overlay", height=300 * 5, width=250 * 4, points="all",
                                             hover_name="Gene names",
                                             title="Distribution of the distance to the median for <br>the protein cluster: {}".format(
                                                 self.cluster_of_interest))

        # determine the layout
    #    distance_to_median_boxplot_figure.update_layout(
#
 #           # setting a black boy around the graph
  #          xaxis=go.layout.XAxis(linecolor='black',
   #                               linewidth=1,
    #                              title="Map",
     #                             mirror=True),
#
 #           yaxis=go.layout.YAxis(linecolor='black',
  #                                linewidth=1,
    #                              mirror=True),
     #   )

        return distance_to_median_boxplot_figure


    def distance_calculation(self):
        """
        The distances to the median profile of the individual proteins, belonging to specified clusters, across the
        fractions will be used to calculate the distance profile (e.g. Manhattan distance).

        Args:
            self:
            requires dataframe (df_allclusters_onlynorm_fracunstacked, single level column), stored as attribute
            (self.df_allclusters_onlynorm_fracunstacked), in which "Fraction" is unstacked. It contains only the
            normalized data of individual protein clusters substracted by the median of the respective protein cluster
            for each fraction.
            markerproteins: dictionary, key: protein cluster, value: set of gene names, corresponding to a specific cluster

        Returns:
            df_distance_noindex: dataframe, index is reset. It contains the column name "distance", in which the e.g.
            Manhattan distances for each individual protein of the specified clusters (see self.markerproteins) are stored
        """

        markerproteins = self.markerproteins
        df_allclusters_onlynorm_fracunstacked = self.df_allclusters_onlynorm_fracunstacked.copy()

        # np.linalg.norm requires array; ord=1: Manhattan distance will be calculated over 5 dimensions (Fractions)
        distance_array = np.linalg.norm(df_allclusters_onlynorm_fracunstacked.to_numpy(), axis=1, ord=1)

        # series is created, that allows finally the formation of a dataframe again
        distance_series = pd.Series(distance_array)

        # new "Column" name = "Distance"
        distance_series.name = "distance"
        distance_series.index = df_allclusters_onlynorm_fracunstacked.index

        # df is created
        df_distance_noindex = distance_series.reset_index()

        self.df_distance_noindex = df_distance_noindex
        
        self.analysis_summary_dict["Manhattan distances"] = df_distance_noindex.to_json() 

        return df_distance_noindex

    
    def distance_boxplot(self):
        """
        A box plot for 1 desired cluster, and across all maps is generated displaying the distribution of the e.g.
        Manhattan distance.

        Args:
            self:
            df_distance_noindex: stored as attribute (self.df_distance_noindex),index is reset.
            It contains the column name "distance", in which the e.g. Manhattan distances for each individual protein
            of the specified clusters (see self.markerproteins) are stored
            map_names: individual map names are stored as an index

        Returns:
            distance_boxplot_figure: boxplot. Along the x-axis the maps, along the y-axis the distances are shown
        """

        map_names = self.map_names

        df_distance_noindex = self.df_distance_noindex

        # "Gene names", "Map", "Cluster" and transferred into the index
        df_distance_map_cluster_gene_in_index = df_distance_noindex.set_index(["Gene names", "Map", "Cluster"])

        # cluster_of_interest = "Proteasome"
        # self.cluster_of_interest=cluster_of_interest

        df_cluster_xmaps_distance_with_index = pd.DataFrame()

        # for each individual map and a defined cluster data will be extracted from the dataframe
        # "df_distance_map_cluster_gene_in_index" and appended to the new dataframe df_cluster_xmaps_distance_with_index
        for maps in map_names:
            plot_try = df_distance_map_cluster_gene_in_index.xs((self.cluster_of_interest, maps),
                                                                level=["Cluster", "Map"], drop_level=False)
            df_cluster_xmaps_distance_with_index = df_cluster_xmaps_distance_with_index.append(plot_try)

        # index will be reset, required by px.box
        df_cluster_xmaps_distance = df_cluster_xmaps_distance_with_index.reset_index()

        # optinal: points=all (= next to each indiviual boxplot the corresponding datapoints are displayed)
        distance_boxplot_figure = px.box(df_cluster_xmaps_distance, x="Map", y="distance",points="all",
                                         hover_name="Gene names",
                                         title="Manhattan distance distribution for <br>the protein cluster: {}".format(
                                             self.cluster_of_interest)
                                         )

        # determine the layout
        distance_boxplot_figure.update_layout(
            autosize=False,
            width=500,
            height=500,

            # setting a black boy around the graph
            xaxis=go.layout.XAxis(linecolor='black',
                                  linewidth=1,
                                  title="Map",
                                  mirror=True),

            yaxis=go.layout.YAxis(linecolor='black',
                                  linewidth=1,
                                  title="distance",
                                  mirror=True),
        )

        return distance_boxplot_figure
        

    
    def results_overview_table(self):
        """
        Dataframe will be created, that provides information about "range", "mean" and "standardeviation",
        given as the column names, based on the data given in df_distance_noindex

        Args:
            df_distance_noindex: stored as attribute (self.df_distance_noindex),index is reset.
            It contains the column name "distance", in which the e.g. Manhattan distances for each individual protein
            of the specified clusters (see self.markerproteins) are stored
            markerproteins
        """
        df_distance_noindex = self.df_distance_noindex
        df_distance_map_cluster_gene_in_index = df_distance_noindex.set_index(["Gene names", "Map", "Cluster"])
        map_names = self.map_names
        markerproteins = self.markerproteins

        df_overview = pd.DataFrame()

        for maps in map_names:
            for clusters in markerproteins:
                plot_try = df_distance_map_cluster_gene_in_index.xs((clusters, maps), level=["Cluster", "Map"],
                                                                    drop_level=False)
                statistic_table = {"range": (plot_try["distance"].max(axis=0)) - (plot_try["distance"].min(axis=0)),
                                   "median": plot_try["distance"].median(axis=0),
                                   "standardeviation": plot_try["distance"].std(axis=0),
                                   "Cluster": clusters,
                                   "Map": maps}
                statistic_series = pd.Series(data=statistic_table)
                df_statistic_table_individual_cluster = pd.DataFrame(statistic_series).T
                df_overview = df_overview.append(df_statistic_table_individual_cluster)

        df_overview.set_index(["Cluster", "Map"], inplace=True)
        df_overview.sort_index(axis=0, level=0, inplace=True)

        self.analysis_summary_dict["Overview table"] = df_overview.reset_index().to_json()
        self.analysed_datasets_dict[self.expname] = self.analysis_summary_dict.copy() 
        self.analysis_summary_dict.clear()
#########################################################################HAS TO GO TO THE BEGINNINg        
        return df_overview

    def read_jsonFile(self):
        """
        Read-out of the JSON-file and currently analysed dataset, stored in "analysed_datasets_dict". It wil create df_distances_combined ("Gene
        names", "Cluster" are stacked; "Map" and Experiment names (are not stored in an additional level name) are unstacked. Layout will be 
        adjusted for distance-plotting.
    
        Args: 
            self.json_dict: contains the dictionary stored in AnalysedDatasets.json
        
        Returns: 
            df_01_filtered_combined: "Fraction" is unstacked; "Experiment", "Gene names", "Map", "Exp_Map" are stacked 
            df_distance_single: no index, column names: "Gene names", "Cluster", "Experiment", "Map", "Exp_Map", "distance"
            df_distance_collapse: no index, column names: "Gene names", "Cluster", "Experiment", "distance"
            unique_proteins_total: dictionary: Experiment_name -> Unique Proteins
            exp_map_names: list of unique Exp_Map - fusions e.g. LFQ_Map1
            exp_names: list of unique Experiment names - e.g. LFQ
        """
        
        json_dict = self.json_dict
        #add experiments that are not stored in AnalysedDAtasets.json for comparison
        try:
            json_dict[i_class.expname] = i_class.analysed_datasets_dict[i_class.expname]
        except:
            pass
    
        acquisition_loaded = []
        unique_proteins_total = {}
        
        for exp_name in json_dict.keys():
            #print(exp_name)
            for data_type in json_dict[exp_name].keys():
                if data_type == "0/1 normalized data" and exp_name == list(json_dict.keys())[0]:
                    #convert into dataframe
                    df_01_combined = pd.read_json(json_dict[exp_name][data_type])
                    #get only 01 normalized data 
                    df_01_combined = df_01_combined.set_index(["Fraction", "Map", "Gene names"])[["normalized profile"]].unstack(["Fraction", "Map"])
                    df_01_combined.rename(columns = {"normalized profile":exp_name}, inplace=True)
        
                elif data_type == "0/1 normalized data" and exp_name != list(json_dict.keys())[0]:
                    df_01_toadd = pd.read_json(json_dict[exp_name][data_type])
                    df_01_toadd = df_01_toadd.set_index(["Fraction", "Map", "Gene names"])[["normalized profile"]].unstack(["Fraction", "Map"])
                    df_01_toadd.rename(columns = {"normalized profile":exp_name}, inplace=True)
                    #dataframes will be concatenated, only proteins/Profiles that are in both df will be retained
                    df_01_combined = pd.concat([df_01_combined, df_01_toadd], axis=1, join='inner')
                    
                elif data_type == "Manhattan distances" and exp_name == list(json_dict.keys())[0]:
                    #convert into dataframe
                    df_distances_combined = pd.read_json(json_dict[exp_name][data_type])
                    #get only 01 normalized data 
                    df_distances_combined = df_distances_combined.set_index(["Map", "Gene names", "Cluster"])[["distance"]].unstack(["Map"])
                    df_distances_combined.rename(columns = {"distance":exp_name}, inplace=True)
        
                elif data_type == "Manhattan distances" and exp_name != list(json_dict.keys())[0]:
                    df_distances_toadd = pd.read_json(json_dict[exp_name][data_type])
                    df_distances_toadd = df_distances_toadd.set_index(["Map", "Gene names", "Cluster"])[["distance"]].unstack(["Map"])
                    df_distances_toadd.rename(columns = {"distance":exp_name}, inplace=True)
                    
                    #dataframes will be concatenated, only proteins/Profiles that are in both df will be retained
                    df_distances_combined = pd.concat([df_distances_combined, df_distances_toadd], axis=1, join='inner')
                
                elif data_type == "Unique Proteins":
                    unique_proteins_total[exp_name] = json_dict[exp_name][data_type]
                    
                #print("  ", data_type)
               # pd.read_json(json_dict["lfq_spec"]["0/1 normalized data"])
                try:
                    for paramters in json_dict[exp_name][data_type].keys():
                        #print("            ", paramters)
                        if paramters=="acquisition":
                            acquisition_loaded.append(json_dict[exp_name][data_type][paramters])
                        #elif parameters=="Non valid profiles":
                except:
                    continue

        #filter for consistently quantified proteins (they have to be in all fractions and all maps)
        df_01_filtered_combined = df_01_combined.dropna()    
        df_01_filtered_combined.columns.names = ["Experiment", "Fraction", "Map"]
        #reframe it to make it ready for PCA
        df_01_filtered_combined = df_01_filtered_combined.stack(["Experiment", "Map"]).swaplevel(0,1, axis=0).dropna(axis=1)
        index_ExpMap = df_01_filtered_combined.index.get_level_values("Experiment")+'_'+df_01_filtered_combined.index.get_level_values("Map")
        index_ExpMap.name = "Exp_Map"
        df_01_filtered_combined.set_index(index_ExpMap, append=True, inplace=True)      
        
        df_distances_combined.columns.names = ["Experiment", "Map"]
        series = df_distances_combined.stack(["Experiment", "Map"])
        series.name = "distance"
        
        df_distance_collapse = series.to_frame().droplevel(level="Map")
        df_distance_collapse.reset_index(inplace=True)
        
        df_distance_single = series.to_frame()
        #fuse Experiment and Map into one column = "Exp_Map"
        index_dist_ExpMap = df_distance_single.index.get_level_values("Experiment")+'_'+df_distance_single.index.get_level_values("Map")
        index_dist_ExpMap.name = "Exp_Map"
        df_distance_single.set_index(index_dist_ExpMap, append=True, inplace=True)
        df_distance_single.reset_index(inplace=True)
        
        
        self.unique_proteins_total = unique_proteins_total
        self.exp_names = list(df_01_filtered_combined.index.get_level_values("Experiment").unique())
        self.exp_map_names = list(index_dist_ExpMap.unique())
        
        self.df_01_filtered_combined = df_01_filtered_combined 
        
        self.df_distance_collapse = df_distance_collapse
        self.df_distance_single = df_distance_single

    
    def perform_pca_comparison(self):
        """PCA will be performed, using logarithmized data.

        Args:
            self.df_01_filtered_combined: "Fraction" is unstacked; "Experiment", "Gene names", "Map", "Exp_Map" are unstacked

        Returns:
            self.df_pca_for_plotting: PCA processed dataframe
                    index: Experiment 	Gene names 	Map 	Exp_Map
                    columns: PC1 	PC2 	PC3
                    contains only marker genes, that are consistent throughout all maps / experiments
        """

        markerproteins = self.markerproteins

        # isolate only logarithmized profile, and unstack "Fraction"
        df_01orlog_fracunstacked = self.df_01_filtered_combined
            
        pca = PCA(n_components=3)

        # df_pca: PCA processed dataframe, containing the columns "PC1", "PC2", "PC3"
        df_pca = pd.DataFrame(pca.fit_transform(df_01orlog_fracunstacked))
        df_pca.columns = ["PC1", "PC2", "PC3"]
        df_pca.index = df_01orlog_fracunstacked.index
        self.df_pca_for_plotting = df_pca

            
            
    def plot_pca_comparison(self):
        """
        A PCA plot for desired experiments (multi_choice) and 1 desired cluster is generated.
        Either the maps for every single experiment are displayed individually or in a combined manner
    
        Args:
            self.df_pca_for_plotting: PCA processed dataframe
                    index: Experiment 	Gene names 	Map 	Exp_Map
                    columns: PC1 	PC2 	PC3
                    contains only marker genes, that are consistent throughout all maps / experiments
    
        Returns:
            pca_figure: PCA plot.
        """
    
        #df_pca_all_marker_cluster_maps = self.df_pca_all_marker_cluster_maps
        #map_or_exp_names = self.map_or_exp_names
        
        df_pca_for_plotting = self.df_pca_for_plotting
        markerproteins = self.markerproteins
        multi_choice = self.multi_choice
        #symbol_pca = None if "symbol_pca" not in kwargs.keys() else kwargs["symbol_pca"]
        
        
        if self.collapse_maps == False:
            map_or_exp_names = df_pca_for_plotting.loc[(multi_choice)].index.get_level_values("Exp_Map").unique()
            level_of_interest = "Exp_Map"
            symbol_pca = "Experiment"     
        else:
            map_or_exp_names = multi_choice
            level_of_interest = "Experiment"
            symbol_pca = None
        
        df_setofproteins_PCA = pd.DataFrame()
        for map_or_exp in map_or_exp_names:
            for marker in markerproteins[self.cluster_of_interest_comparison]:
                if marker not in df_pca_for_plotting.index.get_level_values("Gene names"):
                    continue
                plot_try_pca = df_pca_for_plotting.xs((marker, map_or_exp), level=["Gene names", level_of_interest],
                                                                 drop_level=False)
                df_setofproteins_PCA = df_setofproteins_PCA.append(plot_try_pca)
        try:
            df_setofproteins_PCA.reset_index(inplace=True)
            pca_figure = px.scatter_3d(df_setofproteins_PCA, x="PC1", y="PC2", z="PC3", color=level_of_interest, 
                                       symbol=symbol_pca, hover_data=["Gene names"],
                                      )
                    
            pca_figure.update_layout(autosize=False, width=800, height=500,
                                  title="PCA plot for <br>the protein cluster: {}".format(self.cluster_of_interest_comparison), 
                                    #legend_traceorder="reversed+grouped"
                                    )
        except:
            pca_figure  ="sth went wrong"
    
        return pca_figure
    
    def distance_boxplot_comparison(self):
        """
        A box plot for desired experiments (multi_choice) and 1 desired cluster is generated displaying the distribution of the e.g.
        Manhattan distance.
        Either the maps for every single experiment are displayed individually or in a combined manner.

        Args:
            self:
            multi_choice : list of experiments, that will be displayed
            cluster_of_interest_comparison: cluster which will be analysed
            map_names: individual map names are stored as an index
            df_distance_single: 
                    columns: Gene names 	Cluster 	Experiment 	Map 	Exp_Map 	distance
                    no index
                    "distance": Manhattan distances for each individual protein of the specified clusters (see self.markerproteins) are stored

        Returns:
            distance_boxplot_figure: boxplot. Along the x-axis the maps, along the y-axis the distances are shown
        """
        
        #markerproteins = self.markerproteins
        #symbol_pca = None if "symbol_pca" not in kwargs.keys() else kwargs["symbol_pca"]
        multi_choice = self.multi_choice
        
        if self.collapse_maps == False:
            df_distance_single = self.df_distance_single
            
            #get only values form experiment of interest
            df_distance_single = df_distance_single.loc[df_distance_single['Experiment'].isin(multi_choice)]
            #get only values form cluster of interest
            df_distance_single = df_distance_single.loc[df_distance_single['Cluster'] == self.cluster_of_interest_comparison]
            
            
            individual_distance_boxplot_figure=go.Figure()
            for i, exp in enumerate(df_distance_single["Experiment"].unique()):
                df_plot=df_distance_single[df_distance_single["Experiment"]==exp]
                individual_distance_boxplot_figure.add_trace(go.Box(
                    x=[df_plot["Experiment"], df_plot["Map"]],
                    y=df_plot["distance"],      
                    line=dict(color=self.css_color[i]),#px.colors.sequential.Plasma_r[i]), 
                    #notched=True,
                    name= exp, 
                    hovertext=df_plot["Gene names"],
                ))
            individual_distance_boxplot_figure.update_layout(boxmode="group", xaxis_tickangle=0, 
                                                             title="Manhattan distance distribution for <br>the protein cluster: {}".format(self.cluster_of_interest_comparison),
                                                             autosize=False,
                                                             width=800,
                                                             height=500,
                                                             # setting a black boy around the graph
                                                             xaxis=go.layout.XAxis(linecolor='black',
                                                                                   linewidth=1,
                                                                                   title="Map",
                                                                                   mirror=True),
                                                 
                                                             yaxis=go.layout.YAxis(linecolor='black',
                                                                                   linewidth=1,
                                                                                   title="distance",
                                                                                   mirror=True))
            
            
            return individual_distance_boxplot_figure
        
        # self.collapse_maps == True:    
        else: 
            map_or_exp_names = multi_choice
            level_of_interest = "Experiment"
            boxplot_color = "Experiment"
            df_distance_noindex = self.df_distance_single
    

            # "Gene names", "Map", "Cluster" and transferred into the index
            df_distance_map_cluster_gene_in_index = df_distance_noindex.set_index(["Gene names", level_of_interest, "Cluster"]) ###################level_of_interest
    
            df_cluster_xmaps_distance_with_index = pd.DataFrame()
    
            # for each individual map and a defined cluster data will be extracted from the dataframe
            # "df_distance_map_cluster_gene_in_index" and appended to the new dataframe df_cluster_xmaps_distance_with_index
            for map_or_exp in map_or_exp_names: ###################################################################################################map_or_exp_names
                plot_try = df_distance_map_cluster_gene_in_index.xs((self.cluster_of_interest_comparison, map_or_exp),
                                                                    level=["Cluster", level_of_interest], drop_level=False)
                df_cluster_xmaps_distance_with_index = df_cluster_xmaps_distance_with_index.append(plot_try)
    
            # index will be reset, required by px.box
            df_cluster_xmaps_distance = df_cluster_xmaps_distance_with_index.reset_index()
    
            
            # optinal: points=all (= next to each indiviual boxplot the corresponding datapoints are displayed)
            distance_boxplot_figure = px.box(df_cluster_xmaps_distance, x=level_of_interest, y="distance",#points="all",           ######################level_of_interest
                                             hover_name="Gene names", color = boxplot_color,
                                             title="Global Manhattan distance distribution for <br>the protein cluster: {}".format(
                                                 self.cluster_of_interest_comparison)
                                             )
    
            # determine the layout
            distance_boxplot_figure.update_layout(
                autosize=False,
                width=500,
                height=500,
    
                # setting a black boy around the graph
                xaxis=go.layout.XAxis(linecolor='black',
                                      linewidth=1,
                                      title="Map",
                                      mirror=True),
    
                yaxis=go.layout.YAxis(linecolor='black',
                                      linewidth=1,
                                      title="distance",
                                      mirror=True),
            )
            
            return distance_boxplot_figure

    
    def venn_diagram(self):
        multi_choice_venn = self.multi_choice_venn
        #try:
         #   vd.clear()
        #except:
         #   pass
        #try:
        if len(multi_choice_venn)==2:
            vd = venn2([set(self.unique_proteins_total[i]) for i in multi_choice_venn], 
                 set_labels=([i for i in multi_choice_venn]),
                 set_colors=("#F4ACB7","#c4e6ff")
                 )
        elif len(multi_choice_venn)==3:
            vd = venn3([set(self.unique_proteins_total[i]) for i in multi_choice_venn],
              set_labels=([i for i in multi_choice_venn]),
              set_colors=("#c4e6ff", "#F4ACB7","#9D8189"), 
              alpha = 0.8)
        
        else:
            return ("Please select 2 or more experiments for comparison")
            #venn3_circles([set(unique_proteins_total[i]) for i in multi_choice.value], 
           #                   linestyle="-.", linewidth=2, color="grey")
        #for text in vd.set_labels:
        #    text.set_fontsize(16)
        #for text in vd.subset_labels:
        #    text.set_fontsize(16)
        vd = plt.title("Unique Proteins - Venn Diagram",
                  #fontname="Times New Roman", fontweight="bold",backgroundcolor="#cbe7e3",color="black",style="italic"
                  pad=30,fontsize=20,
                  )
        vd = vd.figure
        out_img = io.BytesIO()
        plt.savefig(out_img, bbox_inches='tight',format='jpg',  dpi = 105)
        out_img.seek(0)  # rewind file
        im = Image.open(out_img)
        plt.clf()
        ##encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
        
            ## A canvas must be manually attached to the figure
            #canvas = FigureCanvas(vd.figure)
            #
            ##Save the figure to a string | draw the canvas, cache the renderer
            #canvas.draw()       
            #
            ##Convert to a NumPy array.
            #buf = canvas.buffer_rgba()
            #X = np.asarray(buf)
            #
            ##Convert to image.
            #venn_diagram = Image.fromarray(X)
        return im        
            
    def svm_processing(self):
        """
        The misclassification matrix, generated by Perseus, will be used for Recall/Precision calculation of each individual cluster and on a global level. 
        Data will be stored in a local dictionary that will be assigned to the global dictionary. 
        
        Args:
            self.df_SVM: dataframe, provided by Perseus, no index; 
                        Column names: e.g. "Predicted: ER", "Predicted: NPC"
                        Rows: e.g. "True: ER", "True: NPC"
        
        Returns:
            self.analysed_datasets_dict:
                local dictionary (SVM_dict) will be assigned to the global dictionary self.analysed_datasets_dict, that is available for downloading
                {"Experiment name" : {...}
                                     {"Misclassification Analysis": 
                                         {
                                          "True: ER" : {
                                                       "Recall": int,
                                                       "FDR": int,
                                                       "Precision": int,
                                                       "F1': int
                                                       }
                                           "True: NPC" : {...}
                                            ...          
                                           "Summary": {...}
                                           }
                                        }
                }
        """
        
        df_SVM = self.df_SVM
        SVM_dict = {}
        all_correct = np.diag(df_SVM)
        members = df_SVM.sum(axis=1)
        total_members = 0
        membrame_members = 0
        membrane_correct = 0
        all_organelle_recall = []
        all_organelle_precision = []
        all_organelle_f1 = []
        F1_all_cluster = []
        no_of_membrane_clusters = 0
        total_correct = sum(all_correct)
        predicted_one_organelle = df_SVM.sum(axis=0)
        
        for i in range(len(df_SVM)):
            total_members = total_members + members[i]
            recall = all_correct[i]/members[i]
            fdr = (predicted_one_organelle[i]-all_correct[i])/predicted_one_organelle[i]
            precision = 1-fdr
            F1 = statistics.harmonic_mean([recall, precision])
            F1_all_cluster.append(F1)
            SVM_dict[df_SVM["T: True group"][i]] = {"Recall": recall, "FDR": fdr, "Precision": precision, "F1": F1}
            if df_SVM["T: True group"][i] != "True: Nuclear pore complex" and df_SVM["T: True group"][i] != "True: Large Protein Complex" and df_SVM["T: True group"][i] != "True: Actin binding proteins" :
                no_of_membrane_clusters = no_of_membrane_clusters+1
                membrame_members = membrame_members + members[i]
                membrane_correct = membrane_correct + all_correct[i]
                all_organelle_f1.append(F1)
                all_organelle_recall.append(recall)
                all_organelle_precision.append(precision)
            
        total_recall = total_correct/total_members
        membrane_recall = membrane_correct/membrame_members
        av_per_organelle_recall = statistics.mean(all_organelle_recall)
        median_per_organelle_recall = statistics.median(all_organelle_recall)
        av_per_organelle_precision = statistics.mean(all_organelle_precision)
        avg_organelle_f1 = statistics.mean(all_organelle_f1)
        avg_F1_all_cluster = statistics.mean(F1_all_cluster)
                    
        SVM_dict["Summary"]={"Total - Recall": total_recall, 
                           "Membrane - Recall" : membrane_recall, 
                           "Av per organelle - Recall": av_per_organelle_recall,
                           "Median per organelle - Recall" : median_per_organelle_recall,
                           "Av precision organelles" : av_per_organelle_precision,
                           "Av F1 organelles" : avg_organelle_f1,
                           "Av F1 all clusters" :  avg_F1_all_cluster,
                          }
        self.analysed_datasets_dict[self.expname]["Misclassification Analysis"] = SVM_dict.copy()
        SVM_dict.clear()
        #self.SVM_dict = SVM_dict    

    def __repr__(self):
        return "This is a spatial dataset with {} lines.".format(len(self.df_original))