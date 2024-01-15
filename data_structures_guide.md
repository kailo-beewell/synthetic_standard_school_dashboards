# Data structures guide for the synthetic standard survey school dashboard

Please note: This will differ for the actual standard survey dashboard, and for the symbol survey and public dashboards.

## Data processing for the synthetic dashboard

### Key:
```mermaid
  graph TD;
    d[(Database)]; 
    r(Dataset);
    i(Data during processing<br>i.e. not available as dataset/csv);
    f{{Function}}

    %% Add custom colour to nodes

    classDef database fill:#b4e1d4;
    class d database;

    classDef process fill:#F7FBFD;
    class i process;

    classDef function fill:#f5e3cb;
    class f function;
    
```

### Figure:
```mermaid
  graph TD;

    %% Define the nodes and subgraphs

    in["Amy completed each of the<br>six versions of the survey"]

    subgraph Within DSH
    
        red[("REDCap DSH")]
    
        red_raw("(1) Raw data from REDCap with seperate columns for the six shuffles")
    
        red_tidy("(2) Cleaned dataset with a single set of REDCap columns<br> and some fake demographic columns")

        head("(3) Headings")

    end

    f_label{{"Function creating dictionary with<br>labels for each of the question responses"}};

    data_sample("Synthetic dataset created by randomly sampling<br>for each of the headings from options in dictionary");

    ons[("Office for National Statistics (ONS)<br>Open Geography Portal")];

    msoa_ew("MSOA shapefile for England + Wales");
    msoa_nd("MSOA shapefile for Northern Devon");

    data_msoa("Dataset with random MSOA for each pupil to the dataset added");
    data_miss("Dataset with some random missing data (for all except school) added<br> and some intentional missing data");
    data_score("Dataset with scores added");

    f_scores{{"Function creating scores"}}

    data_label("Dataset with labels added")

    %% Produce the figure

    in --> red;
    red --> red_raw;
    red_raw --> red_tidy;
    red_tidy --> head;
    head --> data_sample; f_label --> data_sample;
    ons --> msoa_ew;
    msoa_ew --> msoa_nd;
    data_sample --> data_msoa; msoa_nd --> data_msoa;
    data_msoa --> data_miss;
    data_miss --> data_score;
    f_scores --> data_score;
    data_score --> data_label;
    f_label --> data_label;

    %% Add custom colour to nodes

    classDef database fill:#b4e1d4;
    class red,ons database;

    classDef process fill:#F7FBFD;
    class red_tidy,data_sample,data_msoa,data_miss,data_score process;

    classDef function fill:#f5e3cb;
    class f_label,f_scores function;

    classDef transparent fill:transparent, stroke:transparent;
    class in transparent;
```

### Description:

**(1) REDCap data extract:** Pupil survey responses are stored within REDCap on the Data Safe Haven (DSH). Pupils were assigned to one of six survey orders, to mitigate the impact of response fatigue. For example, for a question on acceptance by peers, there will be seven sets of columns - one from the default survey set up ('accept_peer_shuffle') and then six for each of the shuffles ('accept_peer_shuffle_1', 'accept_peer_shuffle_2', ''accept_peer_shuffle_3', 'accept_peer_shuffle_4', 'accept_peer_shuffle_5', and 'accept_peer_shuffle_6'). All the data can be downloaded as a single extract using the "Data Exports, Reports, and Stats" page on REDCap.

**(4) Cleaning the survey responses:** Cleaning is performed using the script `clean_standard_survey.ipynb` on the DSH under Group(S:)/ Kailo_Consortium_BeeWell/ scripts/. This will:
* Create a single set of columns (rather than six columns for the same question)
* Drop pupils if all responses were blank
* Convert answers to numeric (as REDCap answers are numbers but need to change from formatting as strings, '0', '1', etc)
* Set the places and barriers question to NaN if none of the options were chosen (as it was a 'select all that apply' question so requires seperate cleaning based on whether all responses were 0)
* Calculating scores to represent each of the topics in the survey
* Adding label columns for each of the variables in the dataset (so e.g. can translate 0 1 2 to 'Always', 'Sometimes', 'Never')

## Data processing that will be required for the actual dashboards

```mermaid
  graph TD; 
    r(Dataset);
    d[(Database)];
```

```mermaid
  graph TD;

    %% Define the nodes and subgraphs

    dcc[(Devon County Council)]

    subgraph Within DSH

        dem("(1) Pupil demographic data")
    
        red[("REDCap")]
    
        red_raw("(2) Raw data from REDCap<br>with seperate columns for the six shuffles")
    
        red_comb("(3) Raw data + demographic data")
    
        red_tidy("(4) Cleaned dataset with numeric and labelled versions for each<br>survey question or demographic information, and scores for each topic");

    end

    %% Produce the figure

    dcc --> dem;
    dem --> red_comb;
    red --> red_raw;
    red_raw --> red_comb;
    red_comb --> red_tidy;
```

**Combining REDCap and demographic:** Devon County Council are providing demographic data on each of the pupils. The data from Devon County Council is combined with the survey responses based on the pseudonymised UPN associated with each of the survey responses.

## Data fields and types at key stages

### Raw data

### After processing

### For dashboard

### For figure