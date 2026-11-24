# КТ-2. Матрица трассируемости

**Владелец:** Наиль Зарипов. **Версия:** 24.11.2026. **Статус:** PLAN, пока не опубликованы тестовые артефакты и CI SHA. Связь двусторонняя: у каждой истории есть компонент и метод проверки; готовый тест должен ссылаться на требование.

| Требование | Компонент / схема / контракт | Проверка и доказательство | Статус |
| --- | --- | --- | --- |
| US-001 / AC-001/002 | Exec node, NBD block device, job proxy; D-02/D-04; [контракт](../api/operation-spec.md) | AT-001/002, `01-persistent-volume.yson`, два последовательных запуска; лог + SHA | PLAN |
| US-001 / AC-003 | NBD block device, dynamic table; D-05 | AT-003, отказ таблицы и диагностика | PLAN |
| US-002 / AC-004/005/006 | Workspace builder, два volume + bind; D-02/D-04 | AT-004/005, `03-two-volumes.yson`, `findmnt`, SHA контрольных файлов | PLAN |
| US-003 / AC-007/008 | Config postprocessor; D-02 | AT-006/007, `02-invalid-mount.yson` и пересечения | PLAN |
| US-003 / AC-009/010 | Controller agent schema/ACL; D-05 | AT-008/009, отдельные тестовые роли/таблицы | PLAN |
| US-004 / AC-011/012 | Root volume path; D-02/D-03 | AT-010/011, старые спеки на baseline и PR | PLAN |
| NFR-001 | Dynamic table + flush; D-02/D-04, ADR-002 | 20 циклов, SHA-256, PERF-01 | PLAN |
| NFR-002 | Config mount validation; D-02, ADR-003 | AT-004/006/007 | PLAN |
| NFR-003 | Controller agent ACL; D-02/D-05 | AT-008, проверка логов без секретов | PLAN |
| NFR-004 | NBD error path; D-05 | AT-003/012 | PLAN |
| NFR-005 | Exec node + NBD cache; D-03/D-04 | 20 запусков, p95 и RSS | PLAN |
| NFR-006 | Все компоненты legacy path; D-02 | AT-010/011/013, baseline vs PR | PLAN |
| NFR-007 | Build/CI/test environment; D-03, ADR-001 | QUAL-01, чистый checkout и зелёный CI SHA | PLAN |
| NFR-008 | Логи controller/exec/NBD; D-05 | OBS-01, 5 отказов | PLAN |
