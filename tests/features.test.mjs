import assert from 'node:assert/strict';
import { compactImageReferences } from '../patches/mdReferences.ts';
import { formatBeijing, dateKey, formatBeijingTime, formatBeijingFileTime, formatBeijingAttribute, getTimestampDisplayFormatter } from '../patches/beijing.ts';

import { conversationCreateTime, conversationUpdateTime, toUnixSeconds } from '../patches/creation.ts';

const storedConversation = {
    create_time: '2026-03-15T06:54:44Z', // March 15, 14:54:44 Beijing
    update_time: '2026-10-27T06:54:44Z',
    mapping: {
        a: { message: { author: { role: 'user' }, create_time: 1773557684 } },
    },
};
assert.equal(formatBeijingFileTime(new Date(conversationCreateTime(storedConversation) * 1000)), '2026-03-15_14-54-44');
assert.equal(formatBeijingFileTime(new Date(conversationUpdateTime(storedConversation) * 1000)), '2026-10-27_14-54-44');
assert.equal(toUnixSeconds('2026-03-15T06:54:44Z'), toUnixSeconds(1773557684000));
assert.equal(conversationCreateTime({ mapping: {
    a: { message: { author: { role: 'user' }, create_time: '2026-03-15T06:54:44Z' } },
    b: { message: { author: { role: 'assistant' }, create_time: '2026-03-15T06:55:00Z' } },
} }), toUnixSeconds('2026-03-15T06:54:44Z'));
assert.equal(conversationCreateTime({}), 0); // never quietly substitute today's date

const png='data:image/png;base64,aGVsbG8=';
const jpeg='data:image/jpeg;base64,YWJjZA==';
let s=`# title\n\n![题目截图](${png})\n\nanswer\n\n![Again](<${png}>)\n`;
let t=compactImageReferences(s);
assert(t.includes('![题目截图][img-001]'));
assert(t.includes('![Again][img-001]'));
assert.equal((t.match(/\[img-001\]: data:image/g)||[]).length,1);
assert(!t.slice(0,t.indexOf('[img-001]:')).includes('base64'));
assert.equal(t.match(/\[img-\d+\]:/g).length,1);
assert.equal(compactImageReferences('no images'), 'no images');
assert.equal(compactImageReferences('![remote](https://example.com/a.png)'), '![remote](https://example.com/a.png)');
let fence='```markdown\n![code]('+png+')\n```\n![real]('+jpeg+')';
let ft=compactImageReferences(fence);
assert(ft.includes('![code]('+png+')'));
assert(ft.includes('![real][img-001]'));
assert(!ft.includes('[img-002]'));
assert(compactImageReferences('![valid](data:image/png;base64,x)\n`![inline](data:image/png;base64,Zg==)`').includes('`![inline](data:image/png;base64,Zg==)`')); // inline code must stay intact
// Do not hijack existing user-supplied Markdown reference labels.
const userRefs = '[img-001]: https://example.com/original.png\\n\\nExisting ![photo][img-001]\\n\\n![new]('+png+')';
const safeRefs = compactImageReferences(userRefs);
assert(safeRefs.includes('[img-001]: https://example.com/original.png'));
assert(safeRefs.includes('Existing ![photo][img-001]'));
assert(safeRefs.includes('![new][img-002]'));
assert(safeRefs.includes('[img-002]: '+png));
const reservedUsage = compactImageReferences('Some ![image][img-003]\\n\\n![new]('+jpeg+')');
assert(reservedUsage.includes('![new][img-001]'));
const reused = compactImageReferences('![a]('+png+')\\n![b]('+png+')');
assert.equal(reused.split('[img-001]: data:image').length - 1, 1);
const utc=new Date('2026-10-14T17:30:01Z'); // next day 01:30 Beijing
assert.equal(dateKey(utc),'2026-10-15');
assert.equal(formatBeijing(utc),'2026-10-15 01:30:01');
assert.equal(formatBeijingFileTime(utc),'2026-10-15_01-30-01');
assert.equal(formatBeijingAttribute(utc),'2026-10-15T01:30:01+08:00');
assert.equal(formatBeijingTime(utc,false),'01:30:01');
const fm=getTimestampDisplayFormatter(false);
assert.equal(fm(new Date('2026-10-14T15:00:00Z')),'2026-10-14 23:00:00');
assert.equal(fm(new Date('2026-10-14T15:05:00Z')),'23:05:00');
assert.equal(fm(new Date('2026-10-14T16:05:00Z')),'2026-10-15 00:05:00');
console.log('Feature tests PASS');
