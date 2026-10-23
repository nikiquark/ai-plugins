import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import mermaid from 'astro-mermaid';
import { remarkMdLinks } from './src/plugins/remark-md-links.mjs';

const base = '/ai-plugins';

const page = (label, slug) => ({ label, slug });

export default defineConfig({
  site: 'https://nikiquark.github.io',
  base,
  markdown: {
    remarkPlugins: [[remarkMdLinks, { base, docsDir: './src/content/docs' }]],
  },
  integrations: [
    mermaid({ autoTheme: true }),
    starlight({
      title: 'ai-plugins',
      description: 'Документация marketplace плагинов Claude Code nikiquark-ai-plugins',
      defaultLocale: 'root',
      locales: { root: { label: 'Русский', lang: 'ru' } },
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/nikiquark/ai-plugins' }],
      editLink: { baseUrl: 'https://github.com/nikiquark/ai-plugins/edit/main/src/content/docs/' },
      customCss: ['./src/styles/custom.css'],
      plugins: [starlightLinksValidator()],
      sidebar: [
        { label: 'Home', link: '/' },
        {
          label: 'Начало работы',
          items: [
            page('Установка', 'getting-started/installation'),
            page('Quickstart за 2 минуты', 'getting-started/quickstart'),
            page('Первый проект', 'getting-started/first-project'),
            page('Зависимости', 'getting-started/requirements'),
          ],
        },
        {
          label: 'Концепции',
          items: [
            page('Как устроен пайплайн', 'concepts/pipeline'),
            page('Контекст и /clear', 'concepts/context'),
            page('Состояние и возобновление', 'concepts/state'),
            page('Точки решения ✋', 'concepts/gates'),
          ],
        },
        {
          label: 'dev-core',
          items: [
            page('Обзор', 'dev-core'),
            {
              label: 'Скиллы',
              items: [
                page('grill-me', 'dev-core/skills/grill-me'),
                page('review-loop', 'dev-core/skills/review-loop'),
                page('reuse-first', 'dev-core/skills/reuse-first'),
              ],
            },
            page('git-snapshot', 'dev-core/git-snapshot'),
            page('Хук context-guard', 'dev-core/context-guard'),
            page('MCP Context7', 'dev-core/context7'),
          ],
        },
        {
          label: 'web-pipeline',
          items: [
            page('Обзор', 'web-pipeline'),
            {
              label: 'Команды',
              items: [
                page('new-project', 'web-pipeline/commands/new-project'),
                page('change', 'web-pipeline/commands/change'),
                page('deploy', 'web-pipeline/commands/deploy'),
                page('secure-maintain', 'web-pipeline/commands/secure-maintain'),
                page('init', 'web-pipeline/commands/init'),
              ],
            },
            page('Фазы реализации D1–D5', 'web-pipeline/delivery'),
            {
              label: 'Субагенты',
              items: [
                page('Обзор', 'web-pipeline/agents'),
                ...[
                  'content-strategist',
                  'architect',
                  'designer',
                  'backend-dev',
                  'frontend-dev',
                  'qa-engineer',
                  'code-reviewer',
                  'security-reviewer',
                  'design-critic',
                  'ops-auditor',
                ].map((a) => page(a, `web-pipeline/agents/${a}`)),
              ],
            },
            {
              label: 'Навыки-знания',
              items: [
                'frontend-style',
                'seo-standards',
                'backend-standards',
                'testing-standards',
                'ansible-conventions',
              ].map((s) => page(s, `web-pipeline/skills/${s}`)),
            },
            page('Хуки', 'web-pipeline/hooks'),
            page('Конфигурация web-pipeline.json', 'web-pipeline/configuration'),
            page('anti_slop.py', 'web-pipeline/anti-slop'),
            page('seo_check.py', 'web-pipeline/seo-check'),
            page('Шаблоны', 'web-pipeline/templates'),
            page('MCP Playwright', 'web-pipeline/playwright'),
            page('Файлы в проекте', 'web-pipeline/project-files'),
          ],
        },
        {
          label: 'idea-pipeline',
          items: [
            page('Обзор', 'idea-pipeline'),
            {
              label: 'Команды',
              items: ['new-idea', 'evidence', 'readiness', 'interview-kit'].map((c) =>
                page(c, `idea-pipeline/commands/${c}`),
              ),
            },
            {
              label: 'Субагенты',
              items: [
                page('Обзор', 'idea-pipeline/agents'),
                ...[
                  'market-analyst',
                  'competitor-analyst',
                  'customer-researcher',
                  'strategist',
                  'red-team',
                  'fact-checker',
                ].map((a) => page(a, `idea-pipeline/agents/${a}`)),
              ],
            },
            {
              label: 'Навыки-знания',
              items: ['research-standards', 'readiness-levels'].map((s) =>
                page(s, `idea-pipeline/skills/${s}`),
              ),
            },
            page('idea-claims', 'idea-pipeline/idea-claims'),
            page('Конфигурация idea-pipeline.json', 'idea-pipeline/configuration'),
            page('Файлы в проекте', 'idea-pipeline/project-files'),
          ],
        },
        {
          label: 'Справочник',
          items: [
            page('Все команды', 'reference/commands'),
            page('Все агенты', 'reference/agents'),
            page('Переменные окружения', 'reference/environment'),
            page('FAQ и проблемы', 'reference/faq'),
          ],
        },
        {
          label: 'Разработка',
          items: [
            page('Соглашения', 'development/conventions'),
            page('Новый плагин', 'development/new-plugin'),
            page('Валидация и версии', 'development/validation'),
            page('Документация', 'development/docs'),
          ],
        },
      ],
    }),
  ],
});
