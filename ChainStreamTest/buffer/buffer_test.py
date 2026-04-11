import unittest
from chainstream.context.buffer import BufferContext, VideoBuffer, AudioBuffer, TextBuffer, WordBuffer

class TestBufferContext(unittest.TestCase):
    def setUp(self):
        self.buffer = BufferContext(3, 'test')

    def test_init(self):
        self.assertEqual(self.buffer.maxlen, 3)
        self.assertEqual(self.buffer.item_type, 'test')
        self.assertEqual(len(self.buffer.buffer), 0)

    def test_add(self):
        self.buffer.add('item1')
        self.assertEqual(len(self.buffer.buffer), 1)

    def test_get(self):
        self.buffer.add('item1')
        self.assertEqual(self.buffer.get(), 'item1')

    def test_len(self):
        self.buffer.add('item1')
        self.buffer.add('item2')
        self.assertEqual(len(self.buffer), 2)


class TestVideoBuffer(unittest.TestCase):
    def setUp(self):
        self.buffer = VideoBuffer(3)

    def test_init(self):
        self.assertEqual(self.buffer.maxlen, 3)
        self.assertEqual(self.buffer.item_type, 'video')

    def test_save(self):
        self.buffer.save('video1')
        self.assertEqual(len(self.buffer.buffer), 1)

    def test_snapshot(self):
        self.buffer.save('video1')
        self.assertEqual(self.buffer.snapshot(), 'video1')


class TestAudioBuffer(unittest.TestCase):

    def setUp(self):
        self.buffer = AudioBuffer(3)

    def test_init(self):
        self.assertEqual(self.buffer.maxlen, 3)
        self.assertEqual(self.buffer.item_type, 'audio')

    def test_save(self):
        self.buffer.save('audio1')
        self.assertEqual(len(self.buffer.buffer), 1)

    def test_snapshot(self):
        self.buffer.save('audio1')
        self.assertEqual(self.buffer.snapshot(), 'audio1')



class TestTextBuffer(unittest.TestCase):
    # Similar tests as TestVideoBuffer
    def setUp(self):
        self.buffer = TextBuffer(3)

    def test_init(self):
        self.assertEqual(self.buffer.maxlen, 3)
        self.assertEqual(self.buffer.item_type, 'text')

    def test_save(self):
        self.buffer.save('text1')
        self.assertEqual(len(self.buffer.buffer), 1)

    def test_read(self):
        self.buffer.save('text1')
        self.assertEqual(self.buffer.read(), 'text1')


class TestWordBuffer(unittest.TestCase):
    def setUp(self):
        self.buffer = WordBuffer(3)

    def test_init(self):
        self.assertEqual(self.buffer.maxlen, 3)
        self.assertEqual(self.buffer.item_type, 'word')


    def test_save(self):
        self.buffer.save('hellow,chainstream\nhellow')
        self.assertEqual(len(self.buffer.buffer), 3)


    def test_read(self):
        self.buffer.save('hellow,chainstream\nhellow')
        self.assertEqual(self.buffer.read(), 'hellow')


if __name__ == '__main__':
    unittest.main()