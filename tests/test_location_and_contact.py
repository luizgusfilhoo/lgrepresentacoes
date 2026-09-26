"""Institutional story, team contacts, and regional map remain complete."""
from pathlib import Path
import unittest
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
PAGE = html.fromstring((ROOT / 'index.html').read_text(encoding='utf-8'))

class LocationContactTests(unittest.TestCase):
    def test_compact_institutional_story_follows_brands(self):
        main = PAGE.xpath('//main')[0]
        children = [x.get('id') for x in main if x.get('id')]
        self.assertLess(children.index('marcas'), children.index('sobre'))
        section = PAGE.get_element_by_id('sobre')
        content = section.text_content()
        for term in ('Luiz Gustavo Soares Guimarães','Pernambuco','PROPÓSITO','MISSÃO','VISÃO','Ética','Confiança','Excelência','Experiência','Compromisso','Investir em tecnologia'):
            with self.subTest(term=term): self.assertIn(term, content)
        self.assertFalse(section.xpath('.//*[@id="trajetoria"]'))

    def test_all_contacts_and_hours(self):
        section = PAGE.get_element_by_id('contato')
        content = section.text_content()
        for name, digits, email in [('Luiz Filho','5581998940412','contateme.luizfilho@gmail.com'),('Luiz Gustavo','5581998960412','gustavo.lgrep@gmail.com'),('Allyson','5581992136841','allysonandrewwm@outlook.com'),('Manoel','5581998820412','comercial@lgrepresentacoes.com'),('Felipe','5581999857519','comercial@lgrepresentacoes.com')]:
            with self.subTest(name=name):
                self.assertIn(name,content)
                self.assertIn(f'https://wa.me/{digits}',section.xpath('.//a/@href'))
                self.assertIn(f'mailto:{email}',section.xpath('.//a/@href'))
        for day in ('Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado','Domingo'):
            self.assertIn(day,content)
        self.assertEqual(content.count('8h às 18h'),5)
        self.assertIn('8h às 16h',content)
        self.assertIn('8h às 12h',content)

    def test_pernambuco_map_has_text_fallback(self):
        map_area = PAGE.get_element_by_id('pernambuco-map')
        self.assertNotIn('Caruaru',map_area.text_content())
        self.assertIn('Pernambuco',map_area.text_content())
        self.assertIn('www.openstreetmap.org', ''.join(PAGE.xpath('//a/@href')))
        self.assertTrue((ROOT / 'pernambuco-map.js').is_file())
        self.assertNotIn('Caruaru', (ROOT / 'pernambuco-map.js').read_text())
        self.assertNotIn('L.marker(', (ROOT / 'pernambuco-map.js').read_text())
        self.assertTrue((ROOT / 'assets/vendor/leaflet/leaflet.js').is_file())
        self.assertTrue((ROOT / 'assets/vendor/leaflet/leaflet.css').is_file())

if __name__ == '__main__': unittest.main()
