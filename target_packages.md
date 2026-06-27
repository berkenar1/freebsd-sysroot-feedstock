# Target Python Packages for FreeBSD-64 Conda Channel

This document tracks the target Python packages for use with the micromamba FreeBSD port. The packages are organized by their requirements: **Pure Python (noarch)** (runs natively out-of-the-box from standard conda-forge) and **Compiled (freebsd-64)** (requires building for FreeBSD in this feedstock).

---

## 1. Status: Configured in Feedstock (freebsd-64)
These packages contain compiled extensions and are already configured with recipes in this feedstock to build targeting `freebsd-64`:

| Package | Category | Status in Feedstock |
|---------|----------|---------------------|
| `python` | Language Runtime | Configured & Building |
| `numpy` | Numerical Computing / N-D Arrays | Configured & Building |
| `pandas` | Data Manipulation / DataFrames | Configured & Building |
| `sqlite` | database (Python standard library dependency) | Configured & Building |
| `readline` | CLI interface (Python standard library dependency) | Configured & Building |
| `xz` | LZMA compression (Python standard library dependency) | Configured & Building |
| `bzip2` | Bzip2 compression (Python standard library dependency) | Configured & Building |
| `openssl` | Cryptography (Python standard library dependency) | Configured & Building |
| `zlib` | Compression (Python standard library dependency) | Configured & Building |
| `libffi` | Foreign Function Interface (Python standard library dependency) | Configured & Building |
| `openblas` | Optimized BLAS/LAPACK Engine | Configured & Building |

---

## 2. Status: Pure Python (`noarch: python`)
These packages contain only pure Python code and do not have any compiled binary extensions. Their dependencies are either pure Python or libraries listed above. 
**Micromamba on FreeBSD can resolve and install these directly from the official conda-forge channel; no custom build is needed.**

| Package | Downloads/Month / Category |
|---------|----------------------------|
| `boto3` | AWS SDK |
| `packaging` | Build tooling |
| `setuptools` | Build tooling |
| `urllib3` | HTTP client |
| `certifi` | TLS/certificates |
| `typing-extensions` | Type hints |
| `requests` | HTTP client |
| `charset-normalizer` | Encoding detection |
| `idna` | Internationalized domains |
| `botocore` | AWS core SDK |
| `aiobotocore` | Async AWS SDK |
| `python-dateutil` | Date/time utilities |
| `six` | Python 2/3 compat |
| `pycparser` | C parser in Python |
| `pydantic` | Data validation (pure python wrapper) |
| `pluggy` | Plugin system (pytest) |
| `s3transfer` | AWS S3 transfer manager |
| `pygments` | Syntax highlighting |
| `click` | CLI framework |
| `attrs` | Class utilities |
| `anyio` | Async compatibility |
| `fsspec` | Filesystem abstraction |
| `pytest` | Testing framework |
| `h11` | HTTP/1.1 protocol |
| `iniconfig` | INI config parsing |
| `s3fs` | S3 filesystem interface |
| `platformdirs` | Platform-specific dirs |
| `annotated-types` | `Annotated` typing support |
| `pip` | Package installer |
| `wheel` | Python wheel format |
| `jinja2` | Templating engine |
| `jmespath` | JSON query language |
| `importlib-metadata` | Importlib metadata backport |
| `filelock` | Cross-platform file locking |
| `pathspec` | Path pattern matching |
| `pyjwt` | JSON Web Tokens |
| `httpx` | Modern HTTP client |
| `typing-inspection` | Runtime type introspection |
| `python-dotenv` | `.env` file loader |
| `httpcore` | HTTP core transport |
| `pytz` | Timezone definitions |
| `zipp` | Zip path utilities |
| `rich` | Rich terminal output |
| `pyasn1` | ASN.1 types and codecs |
| `jsonschema` | JSON schema validation |
| `google-auth` | Google authentication |
| `markdown-it-py` | Markdown parser |
| `google-api-core` | Google API core |
| `tzdata` | IANA timezone data |
| `tqdm` | Progress bars / utilities |
| `tomli` | TOML parser |
| `colorama` | Cross-platform colors |
| `googleapis-common-protos` | Google API protos |
| `mdurl` | URL utilities for markdown |
| `starlette` | ASGI framework/toolkit |
| `virtualenv` | Virtual environments |
| `awscli` | AWS CLI |
| `trove-classifiers` | PyPI classifiers |
| `fastapi` | Async web framework |
| `rsa` | RSA encryption |
| `referencing` | JSON Schema referencing |
| `pyasn1-modules` | ASN.1 modules |
| `aiosignal` | Async signal callbacks |
| `jsonschema-specifications` | JSON Schema specs |
| `requests-oauthlib` | OAuth for Requests |
| `pyparsing` | Parser combinators |
| `aiohappyeyeballs` | Async Happy Eyeballs |
| `opentelemetry-api` | OpenTelemetry API |
| `tenacity` | Retry library |
| `annotated-doc` | Annotated documentation |
| `cachetools` | Caching utilities |
| `opentelemetry-semantic-conventions` | OTel semantic conventions |
| `hatchling` | Build backend (Hatch) |
| `oauthlib` | OAuth framework |
| `opentelemetry-sdk` | OpenTelemetry SDK |
| `huggingface-hub` | AI/ML Infra |
| `openai` | AI / LLM |
| `langchain` | AI / LLM |
| `openpyxl` | Spreadsheet / Excel |
| `networkx` | Graph / Network Analysis |
| `joblib` | Parallel / Caching |
| `traitlets` | Jupyter / Interactive |
| `transformers` | NLP / Deep Learning |
| `anthropic` | AI / LLM |
| `sympy` | Symbolic Mathematics |
| `datasets` | Data / ML Datasets |
| `threadpoolctl` | Parallel Computing |
| `safetensors` | AI/ML Infra |
| `xlrd` | Spreadsheet / Excel |
| `plotly` | Visualization |
| `notebook` | Jupyter / IDE |
| `altair` | Visualization |
| `jupyterlab` | Jupyter / IDE |
| `seaborn` | Visualization |
| `mlflow` | MLOps |
| `great-expectations` | Data Quality |
| `sentence-transformers` | NLP / Embeddings |
| `wandb` | MLOps / Experiment Tracking |
| `accelerate` | AI/ML Infra |
| `dask` | Parallel / Big Data |
| `xarray` | N-D Arrays / Geoscience |
| `optuna` | Hyperparameter Tuning |
| `llama-index-core` | AI / LLM (RAG) |
| `imbalanced-learn` | Machine Learning |
| `torchmetrics` | Model Evaluation |
| `peft` | AI / LLM Fine-tuning |
| `llama-index` | AI / LLM (RAG) |
| `diffusers` | Generative AI |
| `bokeh` | Visualization |
| `umap-learn` | Dimensionality Reduction (depends on numba) |
| `lightning` | Deep Learning Framework |
| `flax` | Deep Learning / JAX |
| `optax` | Optimization / JAX |
| `pyvis` | Network Visualization |
| `plotnine` | Visualization / ggplot2 |
| `langchain-huggingface` | AI / LLM |
| `numpydoc` | Scientific Documentation |
| `torch-geometric` | Graph ML |
| `phik` | Statistical Correlation |
| `ydata-profiling` | Data Profiling / EDA |
| `arviz` | Bayesian Analysis |
| `sktime` | Time Series ML |
| `evidently` | ML Monitoring |
| `pyjanitor` | Data Cleaning |
| `pycaret` | AutoML |
| `yellowbrick` | ML Visualization |
| `missingno` | Missing Data Visualization |
| `lifelines` | Survival Analysis |
| `hyperopt` | Hyperparameter Tuning |

---

## 3. Status: Custom Compiled Packages Needed (freebsd-64)
These packages contain compiled C/C++/Fortran/Rust/Cython extensions. To make them available for your FreeBSD micromamba environment, custom recipes must be added to this feedstock:

| Package | Category / Sub-dependencies | Build Difficulty |
|---------|-----------------------------|------------------|
| `cryptography` | Crypto primitives (Rust / OpenSSL) | Medium |
| `cffi` | C Foreign Function Interface (C / libffi) | Medium |
| `pyyaml` | YAML parser (C extensions) | Easy |
| `protobuf` | Protocol Buffers (C++ extension) | Medium |
| `pydantic-core` | Rust core for Pydantic v2 | Hard (requires rust toolchain) |
| `markupsafe` | C speedups for HTML escaping | Easy |
| `yarl` | URL parsing (C extension) | Easy |
| `multidict` | Dictionary speedups (C extension) | Easy |
| `aiohttp` | Async HTTP client (C extensions) | Medium |
| `uvicorn` | ASGI server (optional Cython extensions) | Easy |
| `pillow` | Image Processing (C extensions, libjpeg, zlib) | Medium |
| `propcache` | Property caching speedups (C extension) | Easy |
| `frozenlist` | Immutable list speedups (C extension) | Easy |
| `scipy` | Scientific computing (C/C++/Fortran, Meson) | Hard (requires gfortran) |
| `rpds-py` | Rust persistent data structures | Medium (requires rust) |
| `wrapt` | Decorator/monkey-patch speedups (C extension) | Easy |
| `greenlet` | Lightweight coroutines (C extension) | Medium |
| `grpcio` | gRPC Framework (C++ extensions) | Hard |
| `sqlalchemy` | DB ORM (optional C speedups) | Easy |
| `pyarrow` | Apache Arrow columnar library (C++ engine) | Very Hard |
| `regex` | Alternative regex engine (C extension) | Easy |
| `psutil` | System/Process monitoring (C extension) | Medium |
| `lxml` | XML/HTML parser (libxml2, libxslt bindings) | Medium |
| `matplotlib` | Plotting (C++ extensions, freetype, png) | Hard |
| `scikit-learn` | Machine learning (Cython, OpenMP, BLAS) | Hard |
| `tokenizers` | NLP Tokenizers (Rust engine) | Medium (requires rust) |
| `tiktoken` | OpenAI Tokenizer (Rust engine) | Medium (requires rust) |
| `tornado` | Async server (optional C speedups) | Easy |
| `pyzmq` | ZeroMQ bindings (C++ / libzmq) | Medium |
| `torch` | PyTorch Deep Learning (C++ core) | Extremely Hard |
| `numba` | JIT compiler (requires LLVM/llvmlite bindings) | Very Hard |
| `ray` | Distributed runtime (C++ engine) | Extremely Hard |
| `polars` | DataFrames (Rust engine) | Hard (requires rust) |
| `pyspark` | Big Data/Spark (Java integration) | Easy |
| `opencv-python`| Computer Vision (C++ core bindings) | Extremely Hard |
| `duckdb` | OLAP database (C++ engine) | Hard |
| `xgboost` | Gradient boosting (C++ engine) | Hard |
| `h5py` | HDF5 interface (C bindings to libhdf5) | Hard |
| `statsmodels` | Statistical modeling (Cython extensions) | Medium |
| `torchvision` | PyTorch Computer Vision (C++ extensions) | Hard |
| `scikit-image` | Image Processing (Cython extensions) | Medium |
| `tensorflow` | Deep Learning (C++ core) | Extremely Hard |
| `keras` | Deep Learning | Easy (if backend is ready) |
| `spacy` | NLP (Cython extensions, cymem, blis) | Hard |
| `lightgbm` | Gradient boosting (C++ engine) | Hard |
| `jax` | AutoDiff (requires `jaxlib` C++ engine) | Extremely Hard |
| `shap` | Model explainability (C/C++ extensions) | Medium |
| `torchaudio` | PyTorch Audio (C++ extensions) | Hard |
| `kaleido` | Plot export (C++ backend) | Hard |
| `prophet` | Time series forecasting (Stan C++ compilation) | Hard |
| `catboost` | Gradient boosting (C++ engine) | Very Hard |
| `gensim` | Topic modeling (Cython extensions) | Medium |
| `cvxpy` | Optimization (C solvers: SCS, OSQP, ECOS) | Medium |
| `wordcloud` | Word clouds (C extension) | Easy |
| `pymc` | Probabilistic programming (compiles C models) | Medium |
