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
    # Similar tests as TestVideoBuffer
    pass


class TestTextBuffer(unittest.TestCase):
    # Similar tests as TestVideoBuffer
    pass

class TestWordBuffer(unittest.TestCase):
    # Similar tests as TestVideoBuffer, but also test the splitting of words in save method
    pass

if __name__ == '__main__':
    unittest.main()