use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
pub mod sysadmindb_rs {
    use pyo3::exceptions::PyValueError;
    use pyo3::prelude::*;

    use regex::Regex;
    use std::sync::OnceLock;

    fn log_pattern() -> &'static Regex {
        static RE: OnceLock<Regex> = OnceLock::new();
        RE.get_or_init(|| Regex::new(r"<(?<prival>[0-9]+)>(?<version>[0-9])?\s?(?<date>([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+(Z|[+-][0-9]{2}:[0-9]{2})|\w{3}\s[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}))\s(?<hostname>[\w.]+)\s(?<appname>[\w.]+)\s?\[?(?<procid>[0-9-]+)?\]?\:?\s?(?<msgid>(-|\w{2}[0-9]{2}))?\s?(?<structureddata>(\[.+\]|-))?\s?(BOM)?(?<msg>.+)?").unwrap())
    }

    #[pyclass]
    struct Log {
        #[pyo3(get)]
        version: Option<u32>,
        #[pyo3(get)]
        prival: u32,
        #[pyo3(get)]
        date: String,
        #[pyo3(get)]
        hostname: String,
        #[pyo3(get)]
        appname: String,
        #[pyo3(get)]
        procid: String,
        #[pyo3(get)]
        msgid: String,
        #[pyo3(get)]
        structureddata: String,
        #[pyo3(get)]
        msg: String,
    }
    #[pymethods]
    impl Log {
        #[new]
        fn new(line: &str) -> PyResult<Self> {
            parse_log(line)
        }
    }
    fn parse_log(line: &str) -> PyResult<Log> {
        let caps = log_pattern()
            .captures(line)
            .ok_or_else(|| PyValueError::new_err("Cannot parse"))?;

        Ok(Log {
            prival: caps["prival"].parse().unwrap(),
            version: caps.name("version").map(|m| m.as_str().parse().unwrap()),
            date: caps["date"].to_owned(),
            hostname: caps["hostname"].to_owned(),
            appname: caps["appname"].to_owned(),
            procid: caps["procid"].to_owned(),
            msgid: caps["msgid"].to_owned(),
            structureddata: caps["structureddata"].to_owned(),
            msg: caps
                .name("msg")
                .map(|m| m.as_str().to_owned())
                .unwrap_or_default(),
        })
    }
    #[pyfunction]
    fn parse_batch(lines: Vec<String>) -> PyResult<Vec<Log>> {
        lines.iter().map(|l| parse_log(l)).collect()
    }

    #[pyfunction]
    pub fn match_only(line: &str) -> bool {
        // I use capture to simulate matching and capturing without building the struct
        log_pattern().captures(line).is_some()
    }

    #[pyfunction]
    fn parse_no_return(line: &str) {
        // Match and create struct, but don't send it back to python
        let _ = parse_log(line);
    }
}
