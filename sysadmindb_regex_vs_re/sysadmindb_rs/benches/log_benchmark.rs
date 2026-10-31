use criterion::{Criterion, black_box, criterion_group, criterion_main};
use sysadmindb_rs::sysadmindb_rs::match_only;

fn benchmark_parse(c: &mut Criterion) {
    let line = "<34>1 2003-10-11T22:14:15.003Z mymachine.example.com su - ID47 - BOM'su root' failed for lonvick on /dev/pts/8";

    c.bench_function("match_only", |b| b.iter(|| match_only(black_box(line))));
}

criterion_group! {
  name = benches;
  config = Criterion::default().sample_size(10000);
  targets = benchmark_parse
}

criterion_main!(benches);
