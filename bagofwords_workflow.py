import luigi
import glob
import os
from tasks.text_tasks import BagOfWordsFromParsedTask
from tasks.task_helpers import parse_yaml
from tasks.task_helpers import run_init


class BowWorkflow(luigi.Task):
    doc_dir = luigi.Parameter()
    yaml_file = luigi.Parameter()

    start_index = luigi.Parameter(default=0)
    end_index = luigi.Parameter(default=1000)

    def requires(self):
        return [
            BagOfWordsFromParsedTask(
                input_path=f,
                yaml_file=self.yaml_file
            ) for f in self._iterator()
        ]

    def output(self):
        return luigi.LocalTarget('log.txt')

    def run(self):
        print 'running'

    def _iterator(self):
        for f in glob.glob(os.path.join(self.doc_dir, '*.json'))[self.start_index:self.end_index]:
            yield f

    def _configure(self):
        config = parse_yaml(self.yaml_file)
        run_init(config)


if __name__ == '__main__':
    interval = 2000
    for i in xrange(0, 26000, interval):
        w = BowWorkflow(
            doc_dir='testdata/solr_20150320/docs/',
            yaml_file='tasks/bagofwords_20150320.yaml',
            start_index=i,
            end_index=(i + interval)
        )
        luigi.build([w], local_scheduler=True)
