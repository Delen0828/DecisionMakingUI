# DecisionMakingUI

A static decision-making interface presented as a humanitarian aid deployment portal. Select a location on the map to view its assessment, deployment method, related posts, and urgency/trust distributions. The interface uses local JSON files and requires no build step or backend.

## Run locally

From this directory, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://localhost:8000>. Serve the files over HTTP rather than opening `index.html` directly, because the page loads JSON with `fetch()`. Internet access is needed for Leaflet assets and OpenStreetMap tiles.

## HTML configuration

Edit the attributes on the opening `<html>` tag in [index.html](index.html), then reload the page. Boolean flags use the literal strings `"true"` and `"false"`.

| Parameter | Current value | Current behavior |
| --- | --- | --- |
| `data-theme` | `light` | Legacy setting. Dark-theme styling has been removed; changing this attribute does not switch themes. |
| `data-color-encoding` | `true` | Read by a legacy value-formatting helper that is not called by the current rendering code. Does not disable map, post, or distribution colors. |
| `data-approve-is-green` | `false` | `true` sets the approval/rejection CSS variables to green/red instead of blue/gray. Those variables are not used by the current interface, so there is no visible effect. |
| `data-trust-level-high-is-green` | `true` | Read by a legacy source-formatting helper that is not called by the current rendering code. Does not change post trust badges or charts. |
| `data-show-images` | `false` | Legacy setting; no current image-rendering code reads it. Setting it to `true` does not display images. |
| `data-show-source-expand` | `true` | Active. Controls the `[?]` distribution expanders beside urgency, related posts, and post urgency. `false` hides them. Assessment and post text expansion remain available. |
| `data-show-map` | `true` | Legacy setting; the map is initialized unconditionally. Setting it to `false` does not hide the map. |

The macro comment near the top of the HTML describes older intended behavior; the table above reflects the actual implementation.

## Data files

| File | Purpose / fields |
| --- | --- |
| [incident.json](incident.json) | Location records: `Target ID`, `Target Name`, `Target Category`, `Collateral Damage`, `Certainty`, `Suggested Strike Method`, `AI Description`, `latitude`, `longitude`, `radius_m`, and `source_ids`. Legacy field names are retained; the UI labels them as aid locations, urgency, and deployment methods. Incident urgency uses `low`, `mid`, or `high`. |
| [posts_expanded.json](posts_expanded.json) | Posts displayed by the interface: `id`, `incident_id`, `title`, `source`, `source_type`, `content`, `timestamp`, `trust_level`, and `urgency_level`. Trust and urgency use `low`, `medium`, or `high`; timestamps should be parseable dates. |
| [source.json](source.json) | Source metadata: `name`, `type`, `trust_level`, and `description`. Loaded during startup, although the current interface uses distribution expanders rather than the legacy source-details view. |
| [posts.json](posts.json) | Post dataset for testing, deceperated. |

Related posts are matched by an incident's `source_ids` against post `id`, not by `incident_id`. Distribution expanders summarize the loaded dataset, not just the selected location. All three fetched files must load successfully before initialization completes.

## Optional description-generation script

[generate_descriptions.py](generate_descriptions.py) is a legacy helper, independent of the browser interface. Its current prompt uses intelligence/target terminology rather than the portal's humanitarian terminology.

| Parameter | Current value / configuration |
| --- | --- |
| API key | Required `OPENAI_API_KEY` environment variable; |
| Input records | `processed_data.json`, relative to the working directory; this file is not included. |
| Source metadata | `source.json`; each input record needs a `Source` matching a source `name`. |
| Output | `processed_data_with_descriptions.json`; overwritten on each successful run. |
| Model | `gpt-4`, in `generate_ai_description()`. |
| Temperature | `0.7`. |
| Output token limit | `max_tokens=200`. |
| Requested description length | 100 words in the prompt; not programmatically enforced. |
| Request delay | `time.sleep(1)` before each record. |

Install the `openai` Python package in a virtual environment and set `OPENAI_API_KEY` in your environment before running `python3 generate_descriptions.py`. Input records must include `Target Name`, `Target Category`, `Collateral Damage`, `Certainty`, `Suggested Strike Method`, and `Source`. The script adds an `AI Description` field.