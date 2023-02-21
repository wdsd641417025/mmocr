data_root = 'data/wildreceipt'
cache_path = 'data/cache'

train_preparer = dict(
    obtainer=dict(
        type='NaiveDataObtainer',
        cache_path=cache_path,
        files=[
            dict(
                url='https://download.openmmlab.com/mmocr/data/'
                'wildreceipt.tar',
                save_name='wildreceipt.tar',
                md5='2a2c4a1b4777fb4fe185011e17ad46ae',
                split=['train', 'test'],
                content=['image', 'annotation'],
                mapping=[
                    [
                        'wildreceipt/wildreceipt/class_list.txt',
                        'class_list.txt'
                    ],
                    ['wildreceipt/wildreceipt/dict.txt', 'dict.txt'],
                    ['wildreceipt/wildreceipt/train.txt', 'train.txt'],
                    ['wildreceipt/wildreceipt/image_files', 'image_files'],
                ]),
        ]),
    gatherer=dict(
        type='MonoGatherer', an_name='train.txt', img_dir='image_files'),
    parser=dict(type='WildreceiptKIEAnnParser'),
    packer=dict(type='WildReceiptPacker'),
    dumper=dict(type='WildreceiptOpensetDumper'),
)

test_preparer = dict(
    obtainer=dict(
        type='NaiveDataObtainer',
        cache_path=cache_path,
        files=[
            dict(
                url='https://download.openmmlab.com/mmocr/data/'
                'wildreceipt.tar',
                save_name='wildreceipt.tar',
                md5='2a2c4a1b4777fb4fe185011e17ad46ae',
                split=['train', 'test'],
                content=['image', 'annotation'],
                mapping=[
                    [
                        'wildreceipt/wildreceipt/class_list.txt',
                        'class_list.txt'
                    ],
                    ['wildreceipt/wildreceipt/dict.txt', 'dict.txt'],
                    ['wildreceipt/wildreceipt/test.txt', 'test.txt'],
                    ['wildreceipt/wildreceipt/image_files', 'image_files'],
                ]),
        ]),
    gatherer=dict(type='MonoGatherer', an_name='test.txt'),
    parser=dict(type='WildreceiptKIEAnnParser'),
    packer=dict(type='WildReceiptPacker'),
    dumper=dict(type='WildreceiptOpensetDumper'),
)
